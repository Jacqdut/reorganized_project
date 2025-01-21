from firebase_admin import credentials, initialize_app, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase_service_account.json")
initialize_app(cred)

# Test Firestore Connection
db = firestore.client()
try:
    doc_ref = db.collection("test_collection").document()
    doc_ref.set({"test_field": "test_value"})
    print("Firestore connection successful! Test document created.")
except Exception as e:
    print(f"Error connecting to Firestore: {e}")
