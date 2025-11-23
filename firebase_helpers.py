from firebase_config import db  # assuming db is initialized in firebase_config.py

def get_token_from_firestore(firebase_user_id):
    user_doc = db.collection("users").document(firebase_user_id).get()
    if user_doc.exists:
        data = user_doc.to_dict()
        return data.get("fcm_token")  # make sure this field exists in Firestore
    return None

