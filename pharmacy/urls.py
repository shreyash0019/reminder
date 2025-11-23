from django.urls import path
from .views import (
    medicine_list, medicine_detail, medicine_create_update,
    record_sale, low_stock, expired_medicines
)

urlpatterns = [
    path("medicines/", medicine_list),
    path("medicines/<int:pk>/", medicine_detail),
    path("medicines/save/", medicine_create_update),
    path("sale/", record_sale),
    path("medicines/low-stock/", low_stock),
    path("medicines/expired/", expired_medicines),
]
