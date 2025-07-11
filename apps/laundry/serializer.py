from rest_framework import serializers
from .models import LaundryCategory, LaundryInvoice

class LaundryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryCategory
        fields = ['name', 'wash_price', 'iron_price']

class LaundryInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryInvoice
        fields = ['id', 'items_json', 'total_cost', 'order_date', 'delivery_date']
