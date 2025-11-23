from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Reminder
from pharmacy.models import Medicine


# Show all reminders
def reminder_list(request):
    reminders = Reminder.objects.all().order_by("reminder_time")
    return render(request, "reminders/reminder_list.html", {"reminders": reminders})


# Create a reminder
def create_reminder(request):
    if request.method == "POST":
        firebase_patient_id = request.POST.get("firebase_patient_id")
        firebase_caretaker_id = request.POST.get("firebase_caretaker_id")
        medicine_id = request.POST.get("medicine_id")
        dosage = request.POST.get("dosage")
        reminder_time = request.POST.get("reminder_time")

        medicine = get_object_or_404(Medicine, id=medicine_id)

        reminder = Reminder.objects.create(
            firebase_patient_id=firebase_patient_id,
            firebase_caretaker_id=firebase_caretaker_id,
            medicine=medicine,
            dosage=dosage,
            reminder_time=reminder_time
        )
        return redirect("reminder_list")

    medicines = Medicine.objects.all()
    return render(request, "reminders/create_reminder.html", {"medicines": medicines})


# Mark reminder as taken
def mark_taken(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    reminder.is_taken = True
    reminder.save()
    return JsonResponse({"status": "success", "message": "Reminder marked as taken"})


# API to fetch due reminders (for Celery/Firebase)
def due_reminders(request):
    reminders = Reminder.objects.filter(reminder_time__lte=now(), is_sent=False)
    data = [
        {
            "id": r.id,
            "firebase_patient_id": r.firebase_patient_id,
            "firebase_caretaker_id": r.firebase_caretaker_id,
            "medicine": r.medicine.name,
            "dosage": r.dosage,
            "reminder_time": r.reminder_time,
        }
        for r in reminders
    ]
    return JsonResponse(data, safe=False)

from django.utils.timezone import now
from django.http import JsonResponse
from .models import Reminder
from notifications.utils import send_notification
from firebase_helpers import get_token_from_firestore  # adjust import if needed

def due_reminders(request):
    reminders = Reminder.objects.filter(reminder_time__lte=now(), is_sent=False)
    sent_count = 0

    for r in reminders:
        token = get_token_from_firestore(r.firebase_caretaker_id)
        if token:
            send_notification(token, "Medicine Reminder", f"{r.medicine.name} at {r.reminder_time}")
            r.is_sent = True
            r.save()
            sent_count += 1

    return JsonResponse({"status": "success", "notifications_sent": sent_count})

