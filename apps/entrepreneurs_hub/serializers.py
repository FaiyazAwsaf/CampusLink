from rest_framework import serializers
from .models import Product, Storefront, Rating, Owner

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = [
            'owner_id',
            'name',
            'image',
            'bio',
            'phone',
            'email',
            'facebook_url',
            'instagram_url',
            'website_url',
            'joined_date'
        ]

class StorefrontSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_products = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Storefront
        fields = [
            'store_id',
            'owner',
            'name',
            'image',
            'description',
            'established_date',
            'location',
            'return_policy',
            'shipping_info',
            'store_hours',
            'total_sales',
            'created_at',
            'average_rating',
            'total_products',
            'total_reviews'
        ]
        read_only_fields = ['store_id', 'owner']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_total_products(self, obj):
        return obj.get_total_products()

    def get_total_reviews(self, obj):
        return obj.get_total_reviews()

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
