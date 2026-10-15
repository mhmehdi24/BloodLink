"""
BloodLink — Flask application entry point.

Run with:
    python app.py

Then visit http://127.0.0.1:5000/health
"""

from datetime import date, datetime
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)