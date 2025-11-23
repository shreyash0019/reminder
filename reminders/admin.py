from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = (
        "firebase_patient_id",
        "firebase_caretaker_id",
        "medicine",
        "dosage",
        "reminder_time",
        "is_taken",
        "is_sent",
    )
    list_filter = ("is_taken", "is_sent", "reminder_time")
    search_fields = ("firebase_patient_id", "firebase_caretaker_id", "medicine__name")
