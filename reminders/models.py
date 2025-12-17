from django.db import models
from django.conf import settings
from pharmacy.models import Medicine


class Device(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devices"
    )
    fcm_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=20, default="android")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.platform}"


class Reminder(models.Model):
    firebase_patient_id = models.CharField(max_length=100)
    caretaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50)
    reminder_time = models.DateTimeField()
    is_taken = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "firebase_patient_id",
            "medicine",
            "reminder_time"
        )

    def __str__(self):
        return f"{self.firebase_patient_id} - {self.medicine.name}"
