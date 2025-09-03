from django.shortcuts import render
from .models import Product, Storefront, Rating, EntrepreneurOrder, EntrepreneurOrderItem
from .serializers import ProductSerializer, StorefrontSerializer, RatingSerializer, EntrepreneurOrderSerializer, EntrepreneurOrderItemSerializer
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
    permission_classes = [AllowAny] 
    queryset = Product.objects.all()
    lookup_field = 'product_id'

class StorefrontAPIView(APIView):
    permission_classes = [AllowAny] 
    
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
    permission_classes = [AllowAny]  # Allow anonymous access to view storefront details
    queryset = Storefront.objects.all()
    lookup_field = 'store_id'
    permission_classes = [AllowAny]  # Allow public access to view storefront details

class StorefrontProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Allow anonymous access to view storefront products
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
        # Allow all authenticated entrepreneurs to access
        return request.user.is_authenticated and request.user.role == 'entrepreneur'

    def has_object_permission(self, request, view, obj):
        # obj is a Product instance
        return obj.store_id.owner.user == request.user

class IsEntrepreneurOwner(permissions.BasePermission):
    """Allow only entrepreneurs to manage their own storefronts"""
    def has_permission(self, request, view):
        # Allow all authenticated entrepreneurs to access
        return request.user.is_authenticated and request.user.role == 'entrepreneur'

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
        storefront_id = self.request.query_params.get('storefront_id')
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
                storefront = Storefront.objects.get(store_id=storefront_id, owner__user=self.request.user)
            except Storefront.DoesNotExist:
                raise serializers.ValidationError("Invalid storefront")
        else:
            storefront = Storefront.objects.filter(owner__user=self.request.user).first()
            if not storefront:
                raise serializers.ValidationError("You must have at least one storefront to create products")
        
        serializer.save(store_id=storefront)

    def perform_update(self, serializer):
        serializer.save()


class SubmitEntrepreneurOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        items = request.data.get('items', [])
        payment_method = request.data.get('payment_method', 'cash')
        delivery_address = request.data.get('delivery_address', '')
        phone_number = request.data.get('phone_number', '')
        notes = request.data.get('notes', '')
        
        if not items:
            return Response({'error': 'No items provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_amount = 0
        order_items = []
        
        for item in items:
            try:
                product = Product.objects.get(pk=item.get('product_id'))
            except Product.DoesNotExist:
                return Response({'error': f'Product with ID {item.get("product_id")} not found.'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            if not product.availability:
                return Response({'error': f'Product "{product.name}" is not available.'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            quantity = item.get('quantity', 1)
            if quantity <= 0:
                return Response({'error': 'Quantity must be greater than 0.'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            item_total = float(product.price) * quantity
            total_amount += item_total
            order_items.append((product, quantity, product.price))
        
        order = EntrepreneurOrder.objects.create(
            user=user,
            payment_method=payment_method,
            total_amount=total_amount,
            delivery_address=delivery_address,
            phone_number=phone_number,
            notes=notes
        )
        
        for product, quantity, price_at_time in order_items:
            EntrepreneurOrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_time=price_at_time
            )
        
        return Response({
            'success': True,
            'order_id': order.id,
            'total_amount': float(total_amount)
        }, status=status.HTTP_201_CREATED)


class UserEntrepreneurOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = EntrepreneurOrder.objects.filter(user=user).order_by('-created_at')
        
        data = []
        for order in orders:
            order_data = {
                'order_id': order.id,
                'total_amount': float(order.total_amount),
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'payment_method': order.payment_method,
                'delivery_status': order.delivery_status,
                'delivery_address': order.delivery_address,
                'phone_number': order.phone_number,
                'notes': order.notes,
                'items': []
            }
            
            for item in order.items.all():
                order_data['items'].append({
                    'product_id': item.product.product_id,
                    'product_name': item.product.name,
                    'store_name': item.product.store_id.name,
                    'quantity': item.quantity,
                    'price_at_time': float(item.price_at_time),
                    'total_price': float(item.get_total_price()),
                    'product_image': item.product.image
                })
            
            data.append(order_data)
        
        return Response({'orders': data})


class EntrepreneurOrderDetailAPIView(RetrieveAPIView):
    serializer_class = EntrepreneurOrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EntrepreneurOrder.objects.filter(user=self.request.user)
    
    def get_object(self):
        try:
            return EntrepreneurOrder.objects.get(
                id=self.kwargs['order_id'], 
                user=self.request.user
            )
        except EntrepreneurOrder.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({
                'success': False,
                'error': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'order': serializer.data
        })


class UpdateOrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id):
        try:
            order = EntrepreneurOrder.objects.get(id=order_id)
            
            if request.user != order.user:
                return Response({
                    'success': False,
                    'error': 'Permission denied'
                }, status=status.HTTP_403_FORBIDDEN)
            
            new_status = request.data.get('delivery_status')
            if new_status and new_status in ['cancelled']:
                order.delivery_status = new_status
                order.save()
                
                return Response({
                    'success': True,
                    'message': 'Order status updated successfully',
                    'order_id': order.id,
                    'new_status': order.delivery_status
                })
            else:
                return Response({
                    'success': False,
                    'error': 'Invalid status or operation not allowed'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except EntrepreneurOrder.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
