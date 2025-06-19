from rest_framework import serializers
from .models import Product, Storefront

class StorefrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = [
            'store_id',
            'name'
        ]

class ProductSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(read_only = True)
    image = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = Product

        fields = [
            'product_id',
            'store_id',
            'name',
            'image',
            'description',
            'price',
            'availability'
        ]