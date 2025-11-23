# firebase_users_setup.py
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase key path (update if path changes)
FIREBASE_KEY_PATH = r"C:\Users\Admin\Downloads\medicalremindersystem-firebase-adminsdk-fbsvc-1f9d596810.json"

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Dummy users data
users = [
    {
        "name": "John Doe",
        "email": "patient1@example.com",
        "role": "patient",
        "fcm_token": "fcm_token_patient_1234567890"
    },
    {
        "name": "Alice Smith",
        "email": "caretaker1@example.com",
        "role": "caretaker",
        "fcm_token": "fcm_token_caretaker_0987654321"
    },
    {
        "name": "Dr. Ravi Kumar",
        "email": "caretaker2@example.com",
        "role": "caretaker",
        "fcm_token": "fcm_token_caretaker_1122334455"
    }
]


for user in users:
    user_ref = db.collection("users").add(user)
    print(f"✅ Added {user['role']} with ID: {user_ref[1].id}")


# Fetch and print all users
print("\n📌 Current Users in Firebase:")
users_ref = db.collection("users").stream()
for user in users_ref:
    print(f"{user.id} => {user.to_dict()}")
    
    

