from django.db import models
from datetime import date

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
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.quantity_sold > self.medicine.quantity:
            raise ValueError("Not enough stock available")
        self.medicine.quantity -= self.quantity_sold
        self.medicine.save()
        super().save(*args, **kwargs)
