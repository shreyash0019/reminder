from celery import shared_task
from django.utils import timezone
from .models import Reminder
import firebase_admin
from firebase_admin import credentials, firestore, messaging

# Firebase init
FIREBASE_KEY_PATH = r"C:\Users\Admin\Downloads\medicalremindersystem-firebase-adminsdk-fbsvc-1f9d596810.json"
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user_from_firebase(user_id):
    """Fetch user details (name, email, role, device_token) from Firebase by ID"""
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


def send_fcm_notification(token, title, body):
    """Send push notification via Firebase"""
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )
    response = messaging.send(message)
    print("✅ Push notification sent:", response)


@shared_task
def send_reminder_notifications():
    now = timezone.now()  # ✅ fixed parentheses
    reminders = Reminder.objects.filter(reminder_time__lte=now, is_taken=False, is_sent=False)

    for reminder in reminders:
        patient = get_user_from_firebase(reminder.firebase_patient_id)
        caretaker = get_user_from_firebase(reminder.firebase_caretaker_id) if reminder.firebase_caretaker_id else None

        if not patient:
            print(f"⚠️ Patient not found in Firebase: {reminder.firebase_patient_id}")
            continue

        title = f"Medicine Reminder for {patient.get('name', 'Unknown')}"
        body = (
            f"{patient.get('name', 'Patient')} needs to take "
            f"'{reminder.medicine.name}' ({reminder.dosage}) at {reminder.reminder_time}."
        )

        try:
            if caretaker and "device_token" in caretaker:
                send_fcm_notification(caretaker["device_token"], title, body)
            elif "device_token" in patient:  # fallback to patient
                send_fcm_notification(patient["device_token"], title, body)
            else:
                print("⚠️ No device token available for notification.")

            reminder.is_sent = True
            reminder.save()
        except Exception as e:
            print(f"❌ Failed to send notification: {e}")
