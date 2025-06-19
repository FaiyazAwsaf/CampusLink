from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response({
            'success' : True,
            'items' : serializer.data,
            'total_count' : len(serializer.data)
        }, status=status.HTTP_200_OK)