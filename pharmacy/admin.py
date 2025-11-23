from django.contrib import admin
from .models import Medicine, Sale

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "category", "quantity", "expiry_date", "is_expired", "low_stock")
    list_filter = ("company", "category", "expiry_date")
    search_fields = ("name", "company")

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("medicine", "quantity_sold", "sale_date")
    list_filter = ("sale_date",)
