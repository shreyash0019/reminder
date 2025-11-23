from firebase_admin import messaging

def send_reminder_notification(token, medicine_name, dosage):
    """
    Sends a push notification using Firebase Cloud Messaging
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title="💊 Medicine Reminder",
            body=f"Time to take {dosage} of {medicine_name}",
        ),
        token=token,
    )
    response = messaging.send(message)
    print("✅ Notification sent:", response)
    return response
