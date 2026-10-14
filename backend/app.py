"""
BloodLink — Flask application entry point.

Run with:
    python app.py

Then visit http://127.0.0.1:5000/health
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow the frontend to call this API


@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "BloodLink API",
        "version": "1.0",
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)