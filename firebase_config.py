# firebase_config.py
#import firebase_admin
#from firebase_admin import credentials, firestore
#import os

#FIREBASE_KEY_PATH = r"C:\Users\Admin\Downloads\medicalremindersystem-firebase-adminsdk-fbsvc-1f9d596810.json"

#if not firebase_admin._apps:
   # cred = credentials.Certificate(FIREBASE_KEY_PATH)
   # firebase_admin.initialize_app(cred)

db = None #firestore.client()
