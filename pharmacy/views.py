from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Medicine, Sale
from .serializers import MedicineSerializer, SaleSerializer


# =========================
# VIEWSETS (CRUD)
# =========================

class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [AllowAny]


# =========================
# CUSTOM APIs
# =========================

@api_view(["GET"])
def low_stock(request):
    medicines = Medicine.objects.filter(quantity__lte=10)
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def expired_medicines(request):
    expired = [m for m in Medicine.objects.all() if m.is_expired()]
    serializer = MedicineSerializer(expired, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def daily_sales_report(request):
    today = now().date()
    sales = Sale.objects.filter(sale_date__date=today)

    total_amount = 0
    total_quantity = 0
    sales_data = []

    for sale in sales:
        amount = sale.quantity * sale.price
        total_amount += amount
        total_quantity += sale.quantity

        sales_data.append({
            "medicine": sale.medicine.name,
            "company": sale.medicine.company,
            "quantity_sold": sale.quantity,
            "price_per_unit": sale.price,
            "amount": amount,
            "sale_time": sale.sale_date.strftime("%H:%M:%S")
        })

    return Response({
        "date": str(today),
        "total_sales_amount": total_amount,
        "total_quantity_sold": total_quantity,
        "total_transactions": sales.count(),
        "sales": sales_data
    })
