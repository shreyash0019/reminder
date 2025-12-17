from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Reminder, Device
from pharmacy.models import Medicine
from notifications.utils import send_notification
from firebase_helpers import get_token_from_firestore


# -------------------------------
# API: List all reminders
# -------------------------------
@csrf_exempt
def reminder_list(request):
    reminders = Reminder.objects.all().order_by("reminder_time")
    data = []

    for r in reminders:
        data.append({
            "id": r.id,
            "firebase_patient_id": r.firebase_patient_id,
            "medicine_name": r.medicine.name,
            "dosage": r.dosage,
            "reminder_time": r.reminder_time,
            "is_taken": r.is_taken,
            "is_sent": r.is_sent,
            "caretaker": r.caretaker.username if r.caretaker else None,
        })

    return JsonResponse({"reminders": data})


# -------------------------------
# API: Create Reminder
# -------------------------------
@csrf_exempt
def create_reminder(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Handle medicine: fetch by ID or create default if missing
    medicine_id = data.get("medicine_id")
    if medicine_id:
        medicine = get_object_or_404(Medicine, id=medicine_id)
    else:
        medicine, _ = Medicine.objects.get_or_create(
            name="Paracetamol",
            company="ABC Pharma",
            category="Painkiller",
            quantity=100,
            expiry_date="2026-12-31",
            price=10
        )

    reminder, created = Reminder.objects.get_or_create(
        firebase_patient_id=data["firebase_patient_id"],
        medicine=medicine,
        reminder_time=data["reminder_time"],
        defaults={
            "dosage": data.get("dosage", ""),
            "caretaker_id": data.get("caretaker_id")
        }
    )

    return JsonResponse({
        "created": created,
        "id": reminder.id
    })


# -------------------------------
# API: Mark Reminder as Taken
# -------------------------------
@csrf_exempt
def mark_taken(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    reminder.is_taken = True
    reminder.save()
    return JsonResponse({"status": "taken"})


# -------------------------------
# API: Send Due Reminders
# -------------------------------
@csrf_exempt
def due_reminders(request):
    reminders = Reminder.objects.filter(
        reminder_time__lte=now(),
        is_sent=False
    )

    sent_count = 0
    for r in reminders:
        # Patient token
        patient_token = get_token_from_firestore(r.firebase_patient_id)
        if patient_token:
            send_notification(
                patient_token,
                "Medicine Reminder",
                f"{r.medicine.name} at {r.reminder_time}"
            )

        # Caretaker token (if assigned)
        if r.caretaker:
            devices = Device.objects.filter(user=r.caretaker)
            for d in devices:
                send_notification(
                    d.fcm_token,
                    "Patient Reminder",
                    f"{r.firebase_patient_id} needs {r.medicine.name}"
                )

        r.is_sent = True
        r.save()
        sent_count += 1

    return JsonResponse({"sent": sent_count})
