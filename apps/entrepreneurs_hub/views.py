from django.shortcuts import render
from .models import Product, Storefront
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.accounts.decorators import entrepreneur_required
from apps.accounts.models import Roles
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import json

# Create your views here.
class ProductCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'created_at'

class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductCursorPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.query_params.get('category')
        store = self.request.query_params.get('store')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        availability = self.request.query_params.get('availability')

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

        return queryset
    
class ProductDetailsAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

class StorefrontAPIView(APIView):
    def get(self, request):
        store_names = Storefront.objects.values_list("name", flat=True).distinct()
        return Response(store_names)
    


class ProductCategoryAPIView(APIView):
    def get(self, request):
        category_names = Product.objects.values_list("category", flat=True).distinct().order_by("category")
        return Response(category_names)
    
class RecentlyAddedProducts(APIView):
    def get(self, request):
        recent_products = Product.objects.order_by('-created_at')[:10]
        serializer = ProductSerializer(recent_products, many=True)
        return Response(serializer.data)


# Entrepreneur-only endpoints

def entrepreneur_api_required(view_func):
    """Decorator to convert entrepreneur_required for DRF views"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.has_role(Roles.ENTREPRENEUR):
            return Response({
                'success': False,
                'error': 'Permission denied: entrepreneur role required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt
@entrepreneur_required
@require_http_methods(["POST"])
def create_storefront(request):
    """Create a new storefront (Entrepreneur only)"""
    try:
        data = json.loads(request.body)
        
        name = data.get('name')
        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Storefront name is required'
            }, status=400)
        
        storefront = Storefront.objects.create(
            name=name,
            owner=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Storefront created successfully',
            'storefront': {
                'store_id': storefront.store_id,
                'name': storefront.name,
                'owner': storefront.owner.name
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['POST'])
@entrepreneur_api_required
def create_product(request):
    """Create a new product (Entrepreneur only)"""
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['store_id', 'name', 'category', 'description', 'price']
        for field in required_fields:
            if not data.get(field):
                return Response({
                    'success': False,
                    'error': f'{field} is required'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate storefront exists and belongs to current user
        try:
            storefront = Storefront.objects.get(store_id=data['store_id'])
        except Storefront.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Storefront not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the storefront belongs to the current user
        if storefront.owner != request.user:
            return Response({
                'success': False,
                'error': 'Permission denied: You can only create products for your own storefront'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Create product
        product = Product.objects.create(
            store_id=storefront,
            name=data['name'],
            category=data['category'],
            description=data['description'],
            price=data['price'],
            image=data.get('image', 'https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg'),
            availability=data.get('availability', True)
        )
        
        serializer = ProductSerializer(product)
        
        return Response({
            'success': True,
            'message': 'Product created successfully',
            'product': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@entrepreneur_api_required
def update_product(request, product_id):
    """Update a product (Entrepreneur only)"""
    try:
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the product belongs to the current user
        if not product.is_owned_by(request.user):
            return Response({
                'success': False,
                'error': 'Permission denied: You can only edit your own products'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        
        # Update product fields
        if 'name' in data:
            product.name = data['name']
        if 'category' in data:
            product.category = data['category']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'image' in data:
            product.image = data['image']
        if 'availability' in data:
            product.availability = data['availability']
        
        product.save()
        
        serializer = ProductSerializer(product)
        
        return Response({
            'success': True,
            'message': 'Product updated successfully',
            'product': serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@entrepreneur_api_required
def delete_product(request, product_id):
    """Delete a product (Entrepreneur only)"""
    try:
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the product belongs to the current user
        if not product.is_owned_by(request.user):
            return Response({
                'success': False,
                'error': 'Permission denied: You can only delete your own products'
            }, status=status.HTTP_403_FORBIDDEN)
        
        product_name = product.name
        product.delete()
        
        return Response({
            'success': True,
            'message': f'Product "{product_name}" deleted successfully'
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@entrepreneur_api_required
def get_entrepreneur_analytics(request):
    """Get entrepreneur analytics (Entrepreneur only)"""
    try:
        # Filter products to only show those owned by the current user
        user_storefronts = Storefront.objects.filter(owner=request.user)
        user_products = Product.objects.filter(store_id__in=user_storefronts)
        
        total_products = user_products.count()
        available_products = user_products.filter(availability=True).count()
        unavailable_products = total_products - available_products
        total_storefronts = user_storefronts.count()
        
        # Get category distribution for user's products only
        from django.db.models import Count
        category_stats = user_products.values('category').annotate(
            count=Count('category')
        ).order_by('-count')
        
        analytics = {
            'total_products': total_products,
            'available_products': available_products,
            'unavailable_products': unavailable_products,
            'total_storefronts': total_storefronts,
            'availability_rate': (available_products / total_products * 100) if total_products > 0 else 0,
            'category_distribution': list(category_stats)
        }
        
        return Response({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@entrepreneur_api_required
def get_my_storefronts(request):
    """Get current entrepreneur's storefronts"""
    try:
        storefronts = Storefront.objects.filter(owner=request.user)
        data = [{
            'store_id': storefront.store_id,
            'name': storefront.name,
            'owner': storefront.owner.name,
            'product_count': Product.objects.filter(store_id=storefront).count()
        } for storefront in storefronts]
        
        return Response({
            'success': True,
            'storefronts': data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@entrepreneur_api_required
def get_my_products(request):
    """Get current entrepreneur's products"""
    try:
        user_storefronts = Storefront.objects.filter(owner=request.user)
        products = Product.objects.filter(store_id__in=user_storefronts)
        
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            'success': True,
            'products': serializer.data,
            'total_count': products.count()
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)