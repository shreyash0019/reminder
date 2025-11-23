from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from firebase_config import db  # Import Firestore client from your firebase_config.py
import json

# ✅ List all users from Firebase
def list_users(request):
    users_ref = db.collection("users").stream()
    users = [{**user.to_dict(), "id": user.id} for user in users_ref]
    return JsonResponse(users, safe=False)

# ✅ Create a reminder in Firebase
@csrf_exempt
def create_reminder(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reminder_ref = db.collection("reminders").add(data)
            return JsonResponse({"id": reminder_ref[1].id, "message": "✅ Reminder added!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST method allowed"}, status=405)

# ✅ List all reminders from Firebase
def list_reminders(request):
    reminders_ref = db.collection("reminders").stream()
    reminders = [{**r.to_dict(), "id": r.id} for r in reminders_ref]
    return JsonResponse(reminders, safe=False)
