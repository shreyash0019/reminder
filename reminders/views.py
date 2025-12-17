from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Reminder
from pharmacy.models import Medicine
from notifications.utils import send_notification
from firebase_helpers import get_token_from_firestore


@csrf_exempt
def reminder_list(request):
    reminders = Reminder.objects.all().order_by("reminder_time")

    return JsonResponse({
        "reminders": [
            {
                "id": r.id,
                "firebase_patient_id": r.firebase_patient_id,
                "medicine_name": r.medicine.name,
                "dosage": r.dosage,
                "reminder_time": r.reminder_time,
                "is_taken": r.is_taken,
                "is_sent": r.is_sent,
            }
            for r in reminders
        ]
    })


@csrf_exempt
def create_reminder(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    data = json.loads(request.body)

    medicine = get_object_or_404(Medicine, id=data["medicine_id"])

    reminder, created = Reminder.objects.get_or_create(
        firebase_patient_id=data["firebase_patient_id"],
        medicine=medicine,
        reminder_time=data["reminder_time"],
        defaults={
            "dosage": data.get("dosage", "")
        }
    )

    return JsonResponse({
        "created": created,
        "id": reminder.id
    })


@csrf_exempt
def mark_taken(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    reminder.is_taken = True
    reminder.save()
    return JsonResponse({"status": "taken"})


@csrf_exempt
def due_reminders(request):
    reminders = Reminder.objects.filter(
        reminder_time__lte=now(),
        is_sent=False
    )

    sent = 0
    for r in reminders:
        token = get_token_from_firestore(r.firebase_patient_id)
        if token:
            send_notification(
                token,
                "Medicine Reminder",
                f"{r.medicine.name} time"
            )
            r.is_sent = True
            r.save()
            sent += 1

    return JsonResponse({"sent": sent})
