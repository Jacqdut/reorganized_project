import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
cred = credentials.Certificate("firebase_service_account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add documents to the 'defects' collection
data = [
    {
        "name": "Broken Panel",
        "description": "Solar panel has cracks",
        "severity": "high",
    },
    {"name": "Faulty Wiring", "description": "Loose connection", "severity": "medium"},
    {"name": "Damaged Frame", "description": "Frame is bent", "severity": "low"},
]

for i, defect in enumerate(data):
    doc_ref = db.collection("defects").document(f"defect{i+1}")
    doc_ref.set(defect)
    print(f"Added defect{i+1}")
