from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .models import Reminder
from pharmacy.models import Medicine

# Firebase helpers
from notifications.utils import send_notification
from firebase_helpers import get_token_from_firestore


# -------------------------------
#  API: Get all reminders
# -------------------------------
def reminder_list(request):
    reminders = Reminder.objects.all().order_by("reminder_time")
    data = [
        {
            "id": r.id,
            "firebase_patient_id": r.firebase_patient_id,
            "firebase_caretaker_id": r.firebase_caretaker_id,
            "medicine_id": r.medicine.id,
            "medicine_name": r.medicine.name,
            "dosage": r.dosage,
            "reminder_time": r.reminder_time,
            "is_taken": r.is_taken,
            "is_sent": r.is_sent,
        }
        for r in reminders
    ]
    return JsonResponse({"reminders": data}, safe=False)


# -------------------------------
#  API: Create Reminder
# -------------------------------
def create_reminder(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    firebase_patient_id = request.POST.get("firebase_patient_id")
    firebase_caretaker_id = request.POST.get("firebase_caretaker_id")
    medicine_id = request.POST.get("medicine_id")
    dosage = request.POST.get("dosage")
    reminder_time = request.POST.get("reminder_time")

    if not medicine_id:
        return JsonResponse({"error": "medicine_id required"}, status=400)

    medicine = get_object_or_404(Medicine, id=medicine_id)

    reminder = Reminder.objects.create(
        firebase_patient_id=firebase_patient_id,
        firebase_caretaker_id=firebase_caretaker_id,
        medicine=medicine,
        dosage=dosage,
        reminder_time=reminder_time,
    )

    return JsonResponse({"message": "Reminder created", "id": reminder.id})


# -------------------------------
#  API: Mark Taken
# -------------------------------
def mark_taken(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    reminder.is_taken = True
    reminder.save()
    return JsonResponse({"status": "success", "message": "Reminder marked as taken"})


# -------------------------------
#  API: Send Due Reminders to Firebase
# -------------------------------
def due_reminders(request):
    reminders = Reminder.objects.filter(reminder_time__lte=now(), is_sent=False)
    sent_count = 0

    for r in reminders:
        token = get_token_from_firestore(r.firebase_caretaker_id)

        if token:
            send_notification(
                token,
                "Medicine Reminder",
                f"{r.medicine.name} at {r.reminder_time}"
            )
            r.is_sent = True
            r.save()
            sent_count += 1

    return JsonResponse({
        "status": "success",
        "notifications_sent": sent_count
    })
