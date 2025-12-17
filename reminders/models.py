from django.db import models
from pharmacy.models import Medicine

class Reminder(models.Model):
    firebase_patient_id = models.CharField(max_length=100)
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
