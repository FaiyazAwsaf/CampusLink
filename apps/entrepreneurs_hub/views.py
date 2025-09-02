from django.shortcuts import render
from .models import Product, Storefront, Rating, Owner
from .serializers import ProductSerializer, StorefrontSerializer, RatingSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import serializers

# Create your views here.
class ProductPagePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagePagination
    permission_classes = [AllowAny]  # Allow anonymous access to browse products

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.query_params.get('category')
        store = self.request.query_params.get('store')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        availability = self.request.query_params.get('availability')
        ordering = self.request.query_params.get('ordering')

        if category:
            queryset = queryset.filter(category__iexact=category)

        if store:
            queryset = queryset.filter(store_id__name__iexact=store)

        if min_price:
            try:
                min_price=float(min_price)
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass
        
        if max_price:
            try:
                max_price=float(max_price)
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        if availability:
            if availability.lower() == 'true':
                queryset = queryset.filter(availability=True)
            elif availability.lower() == 'false':
                queryset = queryset.filter(availability=False)

        if ordering in ['price', '-price']:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('created_at') 

        return queryset
    
class ProductDetailsAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Allow anonymous access to view product details
    queryset = Product.objects.all()
    lookup_field = 'product_id'

class StorefrontAPIView(APIView):
    permission_classes = [AllowAny]  # Allow anonymous access to view storefronts
    
    def get(self, request):
        store_names = Storefront.objects.values_list("name", flat=True).distinct()
        return Response(store_names)
    
class ProductCategoryAPIView(APIView):
    permission_classes = [AllowAny]  # Allow anonymous access to view categories
    
    def get(self, request):
        category_names = Product.objects.values_list("category", flat=True).distinct().order_by("category")
        return Response(category_names)

class StorefrontsAPIView(ListAPIView):
    serializer_class = StorefrontSerializer
    permission_classes = [AllowAny]  # Allow anonymous access to view storefronts
    pagination_class = None

    def get_queryset(self):
        queryset = Storefront.objects.all()
        return queryset

class StorefrontDetailAPIView(RetrieveAPIView):
    serializer_class = StorefrontSerializer
    queryset = Storefront.objects.all()
    lookup_field = 'store_id'
    permission_classes = [AllowAny]  # Allow public access to view storefront details

class StorefrontProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagePagination
    permission_classes = [AllowAny]  # Allow public access to view storefront products

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        queryset = Product.objects.filter(store_id=store_id)
        
        ordering = self.request.query_params.get('ordering', 'created_at')
        if ordering in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(ordering)
        
        return queryset

class SearchViewAPI(APIView):
    permission_classes = [AllowAny]  # Allow anonymous access to search
    
    def get(self, request):
        query = request.GET.get('query', '').strip()

        if not query:
            return Response([])

        products = Product.objects.filter(name__icontains=query)
        product_data = ProductSerializer(products, many=True).data
        
        return Response(product_data)

    
class RecentlyAddedProducts(APIView):
    permission_classes = [AllowAny]  # Allow anonymous access to view recent products
    
    def get(self, request):
        recent_products = Product.objects.order_by('-created_at')[:10]
        serializer = ProductSerializer(recent_products, many=True)
        return Response(serializer.data)


class ProductRatingsAPIView(APIView):
    permission_classes = [AllowAny]  # Allow anonymous access to view ratings
    
    def get(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            ratings = Rating.objects.filter(product=product).order_by('-created_at')
            serializer = RatingSerializer(ratings, many=True)
            return Response({
                'success': True,
                'ratings': serializer.data,
                'average_rating': product.get_average_rating(),
                'rating_count': product.get_rating_count()
            })
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Product not found'
            }, status=404)


class SubmitRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            
            rating_value = request.data.get('rating')
            review_text = request.data.get('review', '')

            if not rating_value or not (1 <= int(rating_value) <= 5):
                return Response({
                    'success': False,
                    'error': 'Rating must be between 1 and 5'
                }, status=400)

            rating, created = Rating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': rating_value,
                    'review': review_text
                }
            )

            serializer = RatingSerializer(rating)
            return Response({
                'success': True,
                'rating': serializer.data,
                'message': 'Rating updated successfully' if not created else 'Rating submitted successfully',
                'average_rating': product.get_average_rating(),
                'rating_count': product.get_rating_count()
            })

        except Product.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Product not found'
            }, status=404)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)


class IsEntrepreneurAndOwnsStorefront(permissions.BasePermission):
    """Allow only entrepreneurs to manage their own products"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'entrepreneur' and request.user.has_perm('accounts.can_create_products')

    def has_object_permission(self, request, view, obj):
        # obj is a Product instance
        return obj.store_id.owner.user == request.user

class IsEntrepreneurOwner(permissions.BasePermission):
    """Allow only entrepreneurs to manage their own storefronts"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'entrepreneur' and request.user.has_perm('accounts.can_create_products')

    def has_object_permission(self, request, view, obj):
        # obj is a Storefront instance
        return obj.owner.user == request.user

class StorefrontViewSet(viewsets.ModelViewSet):
    serializer_class = StorefrontSerializer
    permission_classes = [IsAuthenticated, IsEntrepreneurOwner]
    lookup_field = 'store_id'  # Use store_id as the lookup field
    ordering = ['store_id']  # Use the correct ordering field from model
    pagination_class = None  # Disable pagination for storefronts
    
    def get_queryset(self):
        # Only show storefronts owned by the current user
        return Storefront.objects.filter(owner__user=self.request.user)
    
    def perform_create(self, serializer):
        # Get or create an Owner instance for the current user
        owner, created = Owner.objects.get_or_create(
            user=self.request.user,
            defaults={
                'name': (
                    self.request.user.get_full_name() or 
                    self.request.user.username or 
                    self.request.user.email.split('@')[0] if self.request.user.email else 
                    f"User_{self.request.user.id}"
                ),
                'email': self.request.user.email or '',
            }
        )
        serializer.save(owner=owner)

class ProductCRUDViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsEntrepreneurAndOwnsStorefront]
    ordering = ['-created_at']  # Set correct ordering field
    pagination_class = None  # Disable pagination for entrepreneur's own products

    def get_queryset(self):
        # Filter by storefront if provided
        storefront_id = self.request.query_params.get('storefront')
        if storefront_id:
            return Product.objects.filter(
                store_id__owner__user=self.request.user,
                store_id=storefront_id
            ).order_by('-created_at')
        # Otherwise show all products from all user's storefronts
        return Product.objects.filter(store_id__owner__user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Get storefront from request data or default to first storefront
        storefront_id = self.request.data.get('storefront_id')
        if storefront_id:
            try:
                storefront = Storefront.objects.get(id=storefront_id, owner__user=self.request.user)
            except Storefront.DoesNotExist:
                raise serializers.ValidationError("Invalid storefront")
        else:
            storefront = Storefront.objects.filter(owner__user=self.request.user).first()
            if not storefront:
                raise serializers.ValidationError("You must have at least one storefront to create products")
        
        serializer.save(store_id=storefront)

    def perform_update(self, serializer):
        # Ensure only updating own products
        serializer.save()