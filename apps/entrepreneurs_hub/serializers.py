from rest_framework import serializers
from .models import Product, Storefront

class StorefrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storefront

        fields = [
            'store_id',
            'name',
            'image'
        ]

class ProductSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(read_only = True)
    store_name = serializers.CharField(source='store_id.name', read_only=True)
    image = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = Product

        fields = [
            'product_id',
            'store_id',
            'store_name',
            'name',
            'image',
            'category',
            'description',
            'price',
            'availability',
            'created_at'
        ]