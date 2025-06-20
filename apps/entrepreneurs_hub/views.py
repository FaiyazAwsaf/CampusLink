from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ProductListAPIView(APIView):
    def get(self, request):
        
        try:
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 10))
        except ValueError:
            return Response({'success' : False, 'message' : 'Invalid page or limit'}, status=status.HTTP_400_BAD_REQUEST)

        offset = (page - 1) * limit

        category = request.GET.get('category')

        products = Product.objects.all()

        if category:
            products = products.filter(category__iexact = category)
            
        paginated_products = products[offset:offset + limit]

        serializer = ProductSerializer(paginated_products, many=True)

        return Response({
            'success' : True,
            'items' : serializer.data,
            'total_count' : len(serializer.data)
        }, status=status.HTTP_200_OK)