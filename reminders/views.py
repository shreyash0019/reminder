from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Reminder
from pharmacy.models import Medicine
from notifications.utils import send_notification


# -------------------------------
#  API: List reminders
# -------------------------------
@csrf_exempt
def reminder_list(request):
    reminders = Reminder.objects.all().order_by("reminder_time")

    data = []
    for r in reminders:
        data.append({
            "id": r.id,
            "firebase_patient_id": r.firebase_patient_id,
            "medicine": r.medicine.name,
            "dosage": r.dosage,
            "reminder_time": r.reminder_time,
            "is_taken": r.is_taken,
            "is_sent": r.is_sent,
        })

    return JsonResponse({"reminders": data})


# -------------------------------
#  API: Create reminder (NO duplicates)
# -------------------------------
@csrf_exempt
def create_reminder(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    firebase_patient_id = body.get("firebase_patient_id")
    medicine_id = body.get("medicine_id")
    dosage = body.get("dosage")
    reminder_time = body.get("reminder_time")

    if not firebase_patient_id or not medicine_id or not reminder_time:
        return JsonResponse({"error": "Missing fields"}, status=400)

    medicine = get_object_or_404(Medicine, id=medicine_id)

    reminder, created = Reminder.objects.get_or_create(
        firebase_patient_id=firebase_patient_id,
        medicine=medicine,
        reminder_time=reminder_time,
        defaults={
            "dosage": dosage,
            "caretaker": request.user if request.user.is_authenticated else None
        }
    )

    if not created:
        return JsonResponse(
            {"message": "Reminder already exists", "id": reminder.id},
            status=200
        )

    return JsonResponse(
        {"message": "Reminder created", "id": reminder.id},
        status=201
    )


# -------------------------------
#  API: Mark as taken
# -------------------------------
@csrf_exempt
def mark_taken(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    reminder.is_taken = True
    reminder.save()
    return JsonResponse({"status": "success"})


# -------------------------------
#  API: Send due reminders
# -------------------------------
@csrf_exempt
def due_reminders(request):
    reminders = Reminder.objects.filter(
        reminder_time__lte=now(),
        is_sent=False,
        caretaker__isnull=False
    )

    sent = 0
    for r in reminders:
        send_notification(
            r.caretaker,
            "Medicine Reminder",
            f"{r.medicine.name} at {r.reminder_time}"
        )
        r.is_sent = True
        r.save()
        sent += 1

    return JsonResponse({
        "status": "success",
        "notifications_sent": sent
    })
