from rest_framework import serializers
from .models import Product, Storefront, Rating, Owner, EntrepreneurOrder, EntrepreneurOrderItem

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


class EntrepreneurOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.URLField(source='product.image', read_only=True)
    store_name = serializers.CharField(source='product.store_id.name', read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = EntrepreneurOrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_image',
            'store_name',
            'quantity',
            'price_at_time',
            'total_price'
        ]
    
    def get_total_price(self, obj):
        return obj.get_total_price()


class EntrepreneurOrderSerializer(serializers.ModelSerializer):
    items = EntrepreneurOrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = EntrepreneurOrder
        fields = [
            'id',
            'user',
            'user_name',
            'user_email',
            'total_amount',
            'created_at',
            'updated_at',
            'payment_method',
            'delivery_status',
            'delivery_address',
            'phone_number',
            'notes',
            'items'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
