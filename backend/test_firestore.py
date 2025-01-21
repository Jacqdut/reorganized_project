import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key
cred = credentials.Certificate("firebase_service_account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
print("Firestore connected successfully!")
