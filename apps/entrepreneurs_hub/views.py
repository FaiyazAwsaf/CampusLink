from django.shortcuts import render
from .models import Product, Storefront
from .serializers import ProductSerializer, StorefrontSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

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

class StorefrontsAPIView(ListAPIView):

    serializer_class = StorefrontSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Storefront.objects.all()
        return queryset
    
class RecentlyAddedProducts(APIView):
    def get(self, request):
        recent_products = Product.objects.order_by('-created_at')[:10]
        serializer = ProductSerializer(recent_products, many=True)
        return Response(serializer.data)