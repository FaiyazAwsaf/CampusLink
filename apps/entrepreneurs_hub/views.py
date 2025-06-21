from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
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

        if category:
            queryset = queryset.filter(category__iexact=category)

        if store:
            queryset = queryset.filter(store_id__name__iexact=store)

        return queryset