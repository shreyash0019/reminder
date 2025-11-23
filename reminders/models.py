from django.db import models
from pharmacy.models import Medicine


class Reminder(models.Model):
    firebase_patient_id = models.CharField(max_length=100, blank=True, null=True)
    firebase_caretaker_id = models.CharField(max_length=100, blank=True, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50)
    reminder_time = models.DateTimeField()
    is_taken = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)   # ✅ to prevent duplicate emails

    def __str__(self):
        return f"Reminder for {self.firebase_patient_id} - {self.medicine.name} at {self.reminder_time}"
