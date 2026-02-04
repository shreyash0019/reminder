from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Medicine, Sale
from .serializers import MedicineSerializer, SaleSerializer


class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]   # ✅ Anyone can access


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [AllowAny]   # ✅ Anyone can access


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Medicine, Sale
from .serializers import MedicineSerializer, SaleSerializer

# Get all medicines
@api_view(["GET"])
def medicine_list(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)


# Get a single medicine
@api_view(["GET"])
def medicine_detail(request, pk):
    try:
        medicine = Medicine.objects.get(pk=pk)
    except Medicine.DoesNotExist:
        return Response({"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MedicineSerializer(medicine)
    return Response(serializer.data)


# Add or update medicine
@api_view(["POST"])
def medicine_create_update(request):
    if "id" in request.data:
        medicine = Medicine.objects.get(id=request.data["id"])
        serializer = MedicineSerializer(medicine, data=request.data, partial=True)
    else:
        serializer = MedicineSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Record a sale (auto reduces stock)
@api_view(["POST"])
def record_sale(request):
    serializer = SaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Sale recorded & stock updated"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Low Stock Alert API
@api_view(["GET"])
def low_stock(request):
    medicines = Medicine.objects.filter(quantity__lte=10)
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)


# Expired Medicine Alert API
@api_view(["GET"])
def expired_medicines(request):
    expired = [m for m in Medicine.objects.all() if m.is_expired()]
    serializer = MedicineSerializer(expired, many=True)
    return Response(serializer.data)


from django.http import JsonResponse
from django.utils.timezone import now
from .models import Sale

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

    return JsonResponse({
        "date": str(today),
        "total_sales_amount": total_amount,
        "total_quantity_sold": total_quantity,
        "total_transactions": sales.count(),
        "sales": sales_data
    })

