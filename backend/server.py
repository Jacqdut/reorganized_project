from flask import Flask, request, jsonify, make_response
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import os
import logging

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load Firebase Admin SDK credentials
FIREBASE_CREDENTIALS_PATH = (
    "/home/jacqdut/combined_project/backend/firebase_service_account.json"
)

if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    logging.error("Firebase credentials file not found. Please verify the path.")
    raise FileNotFoundError(
        f"Firebase credentials file not found at {FIREBASE_CREDENTIALS_PATH}"
    )

try:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    logging.info("Firebase Admin SDK initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing Firebase Admin SDK: {str(e)}")
    raise

# Initialize Flask App
app = Flask(__name__)


# Health Check Route
@app.route("/")
def home():
    return make_response(jsonify({"message": "Welcome to the Advanced API!"}), 200)


# Endpoint to Retrieve Defects
@app.route("/api/defects", methods=["GET"])
def get_defects():
    try:
        db = firestore.client()
        defects_ref = db.collection("defects")
        docs = defects_ref.stream()
        defects = [{doc.id: doc.to_dict()} for doc in docs]

        logging.info("Defects retrieved successfully.")
        return make_response(jsonify(defects), 200)

    except Exception as e:
        logging.error(f"Error retrieving defects: {str(e)}")
        return make_response(jsonify({"error": str(e)}), 500)


# Error Handler for 404
@app.errorhandler(404)
def not_found(error):
    logging.warning(f"404 Not Found: {request.url}")
    return make_response(jsonify({"error": "Not Found"}), 404)


# Error Handler for 500
@app.errorhandler(500)
def internal_error(error):
    logging.error(f"500 Internal Server Error: {str(error)}")
    return make_response(jsonify({"error": "Internal Server Error"}), 500)


if __name__ == "__main__":
    try:
        logging.info("Starting Flask server...")
        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:
        logging.critical(f"Failed to start the Flask server: {str(e)}")
        raise
