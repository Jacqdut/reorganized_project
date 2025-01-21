import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
cred = credentials.Certificate("firebase_service_account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add a new document
doc_ref = db.collection("defects").document("defect2")
doc_ref.set(
    {
        "name": "Broken Panel",
        "description": "Solar panel has cracks",
        "severity": "high",
    }
)

print("Document added successfully!")
