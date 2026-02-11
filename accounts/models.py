from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('patient', 'Patient'),
        ('caretaker', 'Caretaker'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient'   # prevents migration errors
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
