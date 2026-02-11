from django.db import models
from datetime import date
from django.utils.timezone import now

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    shop_name = models.CharField(max_length=100, default="Main Pharmacy")
    location = models.CharField(max_length=100, default="Hospital Store")

    def is_expired(self):
        return self.expiry_date < date.today()

    def low_stock(self):
        return self.quantity <= 10

    def __str__(self):
        return f"{self.name} ({self.company})"


class Sale(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    sale_date = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        # Prevent selling more than stock
        if self.quantity > self.medicine.quantity:
            raise ValueError("Not enough stock available")
        # Reduce stock
        self.medicine.quantity -= self.quantity
        self.medicine.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.name} on {self.sale_date.strftime('%Y-%m-%d %H:%M:%S')}"
