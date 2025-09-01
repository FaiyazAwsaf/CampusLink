from django.shortcuts import render
from .models import Product, Storefront, Rating
from .serializers import ProductSerializer, StorefrontSerializer, RatingSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ProductPagePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagePagination

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
    queryset = Product.objects.all()
    lookup_field = 'product_id'

class StorefrontAPIView(APIView):
    def get(self, request):
        store_names = Storefront.objects.values_list("name", flat=True).distinct()
        return Response(store_names)
    
class ProductCategoryAPIView(APIView):
    def get(self, request):
        category_names = Product.objects.values_list("category", flat=True).distinct().order_by("category")
        return Response(category_names)

class StorefrontsAPIView(ListAPIView):

    serializer_class = StorefrontSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Storefront.objects.all()
        return queryset

class StorefrontDetailAPIView(RetrieveAPIView):
    serializer_class = StorefrontSerializer
    queryset = Storefront.objects.all()
    lookup_field = 'store_id'

class StorefrontProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagePagination

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        queryset = Product.objects.filter(store_id=store_id)
        
        ordering = self.request.query_params.get('ordering', 'created_at')
        if ordering in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(ordering)
        
        return queryset

class SearchViewAPI(APIView):
    def get(self, request):
        query = request.GET.get('query', '').strip()

        if not query:
            return Response([])

        products = Product.objects.filter(name__icontains=query)
        product_data = ProductSerializer(products, many=True).data
        
        return Response(product_data)

    
class RecentlyAddedProducts(APIView):
    def get(self, request):
        recent_products = Product.objects.order_by('-created_at')[:10]
        serializer = ProductSerializer(recent_products, many=True)
        return Response(serializer.data)


class ProductRatingsAPIView(APIView):
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
