from rest_framework import serializers
from .models import Product, Storefront, Rating

class StorefrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storefront

        fields = [
            'store_id',
            'name',
            'image'
        ]

class RatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Rating
        fields = [
            'rating_id',
            'rating',
            'review',
            'user_name',
            'created_at',
            'updated_at'
        ]

class ProductSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(read_only = True)
    store_name = serializers.CharField(source='store_id.name', read_only=True)
    image = serializers.URLField(allow_blank=True, required=False)
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

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
            'created_at',
            'average_rating',
            'rating_count'
        ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()
