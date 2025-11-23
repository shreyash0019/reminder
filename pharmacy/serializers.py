from rest_framework import serializers
from .models import Medicine, Sale

class MedicineSerializer(serializers.ModelSerializer):
    is_expired = serializers.BooleanField(read_only=True)
    low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Medicine
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"
