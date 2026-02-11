from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MedicineViewSet, SaleViewSet, low_stock, expired_medicines, daily_sales_report

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicines')
router.register(r'sales', SaleViewSet, basename='sales')

urlpatterns = [
    path('', include(router.urls)),

    # Custom APIs
    path('medicines/low-stock/', low_stock),
    path('medicines/expired/', expired_medicines),
    path('sales/daily/', daily_sales_report),
]
