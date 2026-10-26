"""
BloodLink — Flask application entry point.

Run with:
    python app.py

Then visit http://127.0.0.1:5000/health
"""

from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)  # Allow the frontend to call this API


# ------------------------------------------------------------
# Health check
# ------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "BloodLink API",
        "version": "1.0",
    })


# ------------------------------------------------------------
# GET /api/donors — list all donors
# ------------------------------------------------------------
@app.route("/api/donors", methods=["GET"])
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
        # ------------------------------------------------------------
# GET /api/match/<requisition_id> — FIFO dispatch algorithm
# ------------------------------------------------------------
@app.route("/api/match/<int:requisition_id>", methods=["GET"])
def match_requisition(requisition_id):
    """Find compatible active bags for a requisition, ordered by FIFO (expiry ASC)."""
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

            # Step 2: FIFO query — compatible active bags, oldest expiry first
            cursor.execute(
                "SELECT UnitID, BagCode, BloodType, ExpiryDate, StorageLocation "
                "FROM Blood_Inventory "
                "WHERE BloodType = %s AND Status = 'Active' "
                "ORDER BY ExpiryDate ASC "
                "LIMIT %s",
                (req["BloodTypeNeeded"], req["UnitsRequired"]),
            )
            bags = cursor.fetchall()

        return jsonify({
            "requisition": req,
            "matches": bags,
            "matched_count": len(bags),
            "requested_count": req["UnitsRequired"],
        })
    finally:
        conn.close()


# ------------------------------------------------------------
# GET /api/analytics/wastage — aggregate wastage stats
# ------------------------------------------------------------
@app.route("/api/analytics/wastage", methods=["GET"])
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
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)