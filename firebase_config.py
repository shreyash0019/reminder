import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Read service account JSON from environment variable
firebase_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

if not firebase_json:
    raise Exception("FIREBASE_SERVICE_ACCOUNT env variable not set")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
