"""
BloodLink — Flask application entry point.

Run with:
    python app.py

Then visit http://127.0.0.1:5000/health
"""

import os
from datetime import date, datetime, timedelta
import pymysql
from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS

try:
    from api.db import get_connection
except ImportError:
    try:
        from db import get_connection
    except ImportError:
        from backend.db import get_connection

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.errorhandler(pymysql.err.OperationalError)
def handle_db_operational_error(e):
    return jsonify({
        "error": "Database Connection Failed",
        "detail": str(e),
        "hint": "Please verify MySQL is running and your .env credentials (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT) are correct."
    }), 503

@app.errorhandler(pymysql.err.MySQLError)
def handle_mysql_error(e):
    return jsonify({
        "error": "Database Query Error",
        "detail": str(e)
    }), 500


# Custom JSON encoder so dates serialize as YYYY-MM-DD (not HTTP-date)
from flask.json.provider import DefaultJSONProvider
from datetime import date as _date, datetime as _datetime

class BloodLinkJSONProvider(DefaultJSONProvider):
    @staticmethod
    def default(o):
        if isinstance(o, (_date, _datetime)):
            return o.isoformat()
        return DefaultJSONProvider.default(o)

app.json = BloodLinkJSONProvider(app)


# ------------------------------------------------------------
# Health check & Root API info
# ------------------------------------------------------------
@app.route("/", methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
@app.route("/api/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint with live database connection diagnostic."""
    db_status = "unknown"
    db_error = None
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = "connected"
        finally:
            conn.close()
    except Exception as e:
        db_status = "disconnected"
        db_error = str(e)

    return jsonify({
        "status": "ok",
        "service": "BloodLink API",
        "version": "1.0",
        "database": {
            "status": db_status,
            "error": db_error
        },
        "endpoints": [
            "/api/health",
            "/api/donors",
            "/api/inventory",
            "/api/patients",
            "/api/requisitions",
            "/api/match/<id>",
            "/api/dispatch",
            "/api/hospitals",
            "/api/analytics/wastage",
            "/api/analytics/demand",
            "/api/analytics/stock"
        ]
    })


# ------------------------------------------------------------
# GET /api/donors — list all donors
# ------------------------------------------------------------
@app.route("/api/donors", methods=["GET"])
@app.route("/donors", methods=["GET"])
def list_donors():
    """Return all donors as a JSON list."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT DonorID, FullName, BloodType, ContactNumber, "
                "DateOfBirth, Gender, LastDonationDate "
                "FROM Donors ORDER BY DonorID"
            )
            donors = cursor.fetchall()
        return jsonify(donors)
    finally:
        conn.close()


# ------------------------------------------------------------
# POST /api/donors — register a new donor (120-day rule)
# ------------------------------------------------------------
@app.route("/api/donors", methods=["POST"])
@app.route("/donors", methods=["POST"])
def create_donor():
    """Register a new donor, enforcing the 120-day recovery rule."""
    data = request.get_json(silent=True) or {}

    # Required fields
    required = ["FullName", "BloodType", "ContactNumber", "DateOfBirth", "Gender"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    # 120-day recovery rule (BR-1)
    last = data.get("LastDonationDate")
    if last:
        try:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "LastDonationDate must be YYYY-MM-DD"}), 400

        days_since = (date.today() - last_date).days
        if days_since < 120:
            return jsonify({
                "error": "Donor not eligible",
                "reason": f"Only {days_since} days since last donation; 120 required.",
                "days_remaining": 120 - days_since,
            }), 400

    # Insert
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Donors "
                "(FullName, BloodType, ContactNumber, DateOfBirth, Gender, LastDonationDate) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    data["FullName"],
                    data["BloodType"],
                    data["ContactNumber"],
                    data["DateOfBirth"],
                    data["Gender"],
                    last,
                ),
            )
            new_id = cursor.lastrowid
        conn.commit()
        return jsonify({"message": "Donor registered", "DonorID": new_id}), 201
    finally:
        conn.close()



# ------------------------------------------------------------
# GET /api/inventory — list blood bags (optionally filter by status)
# ------------------------------------------------------------
@app.route("/api/inventory", methods=["GET"])
@app.route("/inventory", methods=["GET"])
def list_inventory():
    """Return all blood bags. Optional ?status=Active|Dispatched|Discarded."""
    status = request.args.get("status")

    sql = (
        "SELECT UnitID, BagCode, BloodType, DonorID, CollectionDate, "
        "ExpiryDate, Status, StorageLocation "
        "FROM Blood_Inventory"
    )
    params = ()
    if status:
        sql += " WHERE Status = %s"
        params = (status,)
    sql += " ORDER BY ExpiryDate ASC"

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        conn.close()
 # ------------------------------------------------------------
# POST /api/inventory — register a new blood bag (42-day expiry)
# ------------------------------------------------------------
@app.route("/api/inventory", methods=["POST"])
@app.route("/inventory", methods=["POST"])
def create_inventory():
    """Register a new blood bag. ExpiryDate = CollectionDate + 42 days."""
    data = request.get_json(silent=True) or {}

    # Required fields
    required = ["BagCode", "BloodType", "CollectionDate"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    # Parse collection date
    try:
        collection_date = datetime.strptime(data["CollectionDate"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "CollectionDate must be YYYY-MM-DD"}), 400

    # 42-day expiry engine (BR-2)
    expiry_date = collection_date + timedelta(days=42)

    # Insert
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Blood_Inventory "
                "(BagCode, BloodType, DonorID, CollectionDate, ExpiryDate, "
                " Status, StorageLocation) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    data["BagCode"],
                    data["BloodType"],
                    data.get("DonorID"),
                    collection_date,
                    expiry_date,
                    "Active",
                    data.get("StorageLocation"),
                ),
            )
            new_id = cursor.lastrowid
        conn.commit()
        return jsonify({
            "message": "Blood bag registered",
            "UnitID": new_id,
            "ExpiryDate": expiry_date.isoformat(),
        }), 201
    finally:
        conn.close() 
        # ------------------------------------------------------------
# PATCH /api/inventory/<id> — soft-delete or status update
# ------------------------------------------------------------
@app.route("/api/inventory/<int:unit_id>", methods=["PATCH"])
@app.route("/inventory/<int:unit_id>", methods=["PATCH"])
def update_inventory(unit_id):
    """Update a bag's status. Valid: Active, Dispatched, Discarded."""
    data = request.get_json(silent=True) or {}
    new_status = data.get("Status")

    if new_status not in ("Active", "Dispatched", "Discarded"):
        return jsonify({
            "error": "Invalid status",
            "allowed": ["Active", "Dispatched", "Discarded"],
        }), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Blood_Inventory SET Status = %s WHERE UnitID = %s",
                (new_status, unit_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                return jsonify({"error": "Unit not found", "UnitID": unit_id}), 404
        conn.commit()
        return jsonify({"message": "Status updated", "UnitID": unit_id, "Status": new_status})
    finally:
        conn.close()


# ------------------------------------------------------------
# GET /api/requisitions — list hospital requisitions
# ------------------------------------------------------------
@app.route("/api/requisitions", methods=["GET"])
@app.route("/requisitions", methods=["GET"])
def list_requisitions():
    """Return all requisitions. Optional ?status=Pending|Approved|Fulfilled|Rejected."""
    status = request.args.get("status")

    sql = (
        "SELECT RequisitionID, HospitalID, BloodTypeNeeded, UnitsRequired, "
        "UrgencyLevel, Status, RequestedAt "
        "FROM Hospital_Requisitions"
    )
    params = ()
    if status:
        sql += " WHERE Status = %s"
        params = (status,)
    sql += " ORDER BY RequestedAt ASC"

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        conn.close()


# ------------------------------------------------------------
# POST /api/requisitions — create a hospital requisition
# ------------------------------------------------------------
@app.route("/api/requisitions", methods=["POST"])
@app.route("/requisitions", methods=["POST"])
def create_requisition():
    """Create a new hospital requisition (emergency blood request)."""
    data = request.get_json(silent=True) or {}

    required = ["HospitalID", "BloodTypeNeeded", "UnitsRequired"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    try:
        units = int(data["UnitsRequired"])
        if units <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "UnitsRequired must be a positive integer"}), 400

    urgency = data.get("UrgencyLevel", "Standard")
    if urgency not in ("Standard", "Urgent", "Critical"):
        return jsonify({"error": "UrgencyLevel must be Standard, Urgent, or Critical"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Hospital_Requisitions "
                "(HospitalID, BloodTypeNeeded, UnitsRequired, UrgencyLevel, Status) "
                "VALUES (%s, %s, %s, %s, %s)",
                (data["HospitalID"], data["BloodTypeNeeded"], units, urgency, "Pending"),
            )
            new_id = cursor.lastrowid
        conn.commit()
        return jsonify({
            "message": "Requisition created",
            "RequisitionID": new_id,
            "Status": "Pending",
        }), 201
    finally:
        conn.close()


# Red Blood Cell (RBC) compatibility table
# Key: Recipient blood type, Value: List of donor blood types (exact match first)
RBC_COMPATIBILITY = {
    "A+":  ["A+", "A-", "O+", "O-"],
    "A-":  ["A-", "O-"],
    "B+":  ["B+", "B-", "O+", "O-"],
    "B-":  ["B-", "O-"],
    "AB+": ["AB+", "AB-", "A+", "A-", "B+", "B-", "O+", "O-"],
    "AB-": ["AB-", "A-", "B-", "O-"],
    "O+":  ["O+", "O-"],
    "O-":  ["O-"],
}


# ------------------------------------------------------------
# GET /api/hospitals — list all hospitals
# ------------------------------------------------------------
@app.route("/api/hospitals", methods=["GET"])
@app.route("/hospitals", methods=["GET"])
def list_hospitals():
    """Return all registered hospitals."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT HospitalID, HospitalName, Location, ContactPerson, ContactNumber "
                "FROM Hospitals ORDER BY HospitalName"
            )
            hospitals = cursor.fetchall()
        return jsonify(hospitals)
    finally:
        conn.close()


# ------------------------------------------------------------
# GET /api/match/<requisition_id> — FIFO dispatch algorithm with RBC compatibility
# ------------------------------------------------------------
@app.route("/api/match/<int:requisition_id>", methods=["GET"])
@app.route("/match/<int:requisition_id>", methods=["GET"])
def match_requisition(requisition_id):
    """Find compatible active bags for a requisition, ordered by FIFO (expiry ASC) and exact match priority."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Step 1: fetch the requisition
            cursor.execute(
                "SELECT RequisitionID, HospitalID, BloodTypeNeeded, UnitsRequired, "
                "UrgencyLevel, Status FROM Hospital_Requisitions WHERE RequisitionID = %s",
                (requisition_id,),
            )
            req = cursor.fetchone()

            if not req:
                return jsonify({"error": "Requisition not found", "RequisitionID": requisition_id}), 404

            if req["Status"] != "Pending":
                return jsonify({
                    "error": "Requisition is not Pending",
                    "current_status": req["Status"],
                }), 400

            # Step 2: FIFO query with RBC compatibility — compatible active bags, oldest expiry first
            needed_type = req["BloodTypeNeeded"]
            compatible_types = RBC_COMPATIBILITY.get(needed_type, [needed_type])
            placeholders = ", ".join(["%s"] * len(compatible_types))

            sql = (
                f"SELECT UnitID, BagCode, BloodType, ExpiryDate, StorageLocation, "
                f"(CASE WHEN BloodType = %s THEN 1 ELSE 0 END) AS IsExactMatch "
                f"FROM Blood_Inventory "
                f"WHERE BloodType IN ({placeholders}) AND Status = 'Active' "
                f"ORDER BY IsExactMatch DESC, ExpiryDate ASC "
                f"LIMIT %s"
            )
            params = (needed_type, *compatible_types, req["UnitsRequired"])

            cursor.execute(sql, params)
            bags = cursor.fetchall()

        return jsonify({
            "requisition": req,
            "matches": bags,
            "matched_count": len(bags),
            "requested_count": req["UnitsRequired"],
            "compatible_types": compatible_types,
        })
    finally:
        conn.close()


# ------------------------------------------------------------
# ------------------------------------------------------------
# POST /api/dispatch — execute dispatch of matched blood bags
# ------------------------------------------------------------
@app.route("/api/dispatch", methods=["POST"])
@app.route("/dispatch", methods=["POST"])
def dispatch_requisition():
    """Fulfill a requisition by dispatching specified active blood bags."""
    data = request.get_json(silent=True) or {}
    req_id = data.get("RequisitionID")
    unit_ids = data.get("UnitIDs") or []

    if not req_id or not unit_ids:
        return jsonify({"error": "RequisitionID and UnitIDs (array of ints) are required"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Verify requisition is still Pending
            cursor.execute(
                "SELECT RequisitionID, Status, UnitsRequired FROM Hospital_Requisitions WHERE RequisitionID = %s",
                (req_id,),
            )
            req = cursor.fetchone()
            if not req:
                return jsonify({"error": "Requisition not found"}), 404
            if req["Status"] != "Pending":
                return jsonify({"error": f"Requisition is already {req['Status']}"}), 400

            # Update bags to Dispatched
            placeholders = ", ".join(["%s"] * len(unit_ids))
            cursor.execute(
                f"UPDATE Blood_Inventory SET Status = 'Dispatched' "
                f"WHERE UnitID IN ({placeholders}) AND Status = 'Active'",
                tuple(unit_ids),
            )
            updated_count = cursor.rowcount
            if updated_count == 0:
                conn.rollback()
                return jsonify({"error": "Selected units are no longer active or do not exist"}), 400

            # Mark requisition fulfilled
            cursor.execute(
                "UPDATE Hospital_Requisitions SET Status = 'Fulfilled' WHERE RequisitionID = %s",
                (req_id,),
            )
        conn.commit()
        return jsonify({
            "message": "Dispatch successful",
            "RequisitionID": req_id,
            "DispatchedCount": updated_count,
            "Status": "Fulfilled",
        })
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ------------------------------------------------------------
# GET /api/analytics/wastage — aggregate wastage stats
# ------------------------------------------------------------
@app.route("/api/analytics/wastage", methods=["GET"])
@app.route("/analytics/wastage", methods=["GET"])
def analytics_wastage():
    """Return aggregate stock and wastage metrics."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Per-status counts
            cursor.execute(
                "SELECT Status, COUNT(*) AS cnt "
                "FROM Blood_Inventory GROUP BY Status"
            )
            status_counts = {row["Status"]: row["cnt"] for row in cursor.fetchall()}

            active = status_counts.get("Active", 0)
            dispatched = status_counts.get("Dispatched", 0)
            discarded = status_counts.get("Discarded", 0)
            total = active + dispatched + discarded

            # Wastage percentage
            wastage_pct = round((discarded / total * 100), 2) if total > 0 else 0.0

            # Stock by blood type (Active only)
            cursor.execute(
                "SELECT BloodType, COUNT(*) AS cnt "
                "FROM Blood_Inventory WHERE Status = 'Active' "
                "GROUP BY BloodType ORDER BY BloodType"
            )
            stock_by_type = cursor.fetchall()

        return jsonify({
            "totals": {
                "active": active,
                "dispatched": dispatched,
                "discarded": discarded,
                "grand_total": total,
            },
            "wastage_percentage": wastage_pct,
            "stock_by_blood_type": stock_by_type,
        })
    finally:
        conn.close()   


# ------------------------------------------------------------
# GET /api/patients — list all patient cases
# ------------------------------------------------------------
@app.route("/api/patients", methods=["GET"])
@app.route("/patients", methods=["GET"])
def list_patients():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT CaseID, PatientName, BloodTypeNeeded, UnitsRequired, "
                "DirectedDonorID, Status, OpenedAt "
                "FROM Patient_Cases ORDER BY OpenedAt DESC"
            )
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        conn.close()


# ------------------------------------------------------------
# POST /api/patients — create a new patient case
# ------------------------------------------------------------
@app.route("/api/patients", methods=["POST"])
@app.route("/patients", methods=["POST"])
def create_patient():
    data = request.get_json(silent=True) or {}
    
    required = ["PatientName", "BloodTypeNeeded", "UnitsRequired"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    try:
        units = int(data["UnitsRequired"])
        if units <= 0: raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "UnitsRequired must be a positive integer"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Patient_Cases (PatientName, BloodTypeNeeded, UnitsRequired, DirectedDonorID, Status) "
                "VALUES (%s, %s, %s, %s, 'Open')",
                (data["PatientName"], data["BloodTypeNeeded"], units, data.get("DirectedDonorID"))
            )
            new_id = cursor.lastrowid
        conn.commit()
        return jsonify({"message": "Patient case created", "CaseID": new_id}), 201
    finally:
        conn.close()


# ------------------------------------------------------------
# Static files fallback routes (for serverless and local)
# ------------------------------------------------------------
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_STATIC_DIRS = [
    os.path.join(_BASE_DIR, "..", "public"),
    os.path.join(_BASE_DIR, "..", "frontend"),
    os.path.join(_BASE_DIR, "public"),
    os.path.join(_BASE_DIR, "frontend"),
]

def _find_file(filename):
    for d in _STATIC_DIRS:
        full_path = os.path.join(d, filename)
        if os.path.isfile(full_path):
            return d, filename
    return None, None

@app.route("/<string:page>.html", methods=["GET"])
def serve_html(page):
    target = f"{page}.html"
    d, f = _find_file(target)
    if d and f:
        return send_from_directory(d, f)
    return jsonify({"error": f"Page {target} not found"}), 404

@app.route("/frontend/<path:filename>", methods=["GET"])
def serve_frontend_dir(filename):
    d, f = _find_file(filename)
    if d and f:
        return send_from_directory(d, f)
    return jsonify({"error": f"File frontend/{filename} not found"}), 404

@app.route("/api.js", methods=["GET"])
def serve_api_js():
    d, f = _find_file("api.js")
    if d and f:
        return send_from_directory(d, f)
    return jsonify({"error": "api.js not found"}), 404


# ------------------------------------------------------------
# Custom 404 error handler with route hints
# ------------------------------------------------------------
@app.errorhandler(404)
def handle_404(e):
    return jsonify({
        "error": "Route Not Found",
        "path": request.path,
        "method": request.method,
        "available_endpoints": [
            "/api/health",
            "/api/donors",
            "/api/inventory",
            "/api/patients",
            "/api/requisitions",
            "/api/match/<requisition_id>",
            "/api/dispatch",
            "/api/hospitals",
            "/api/analytics/wastage"
        ],
        "hint": "Static screens are accessible at /S0-login.html, /S1-dashboard.html, etc."
    }), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)