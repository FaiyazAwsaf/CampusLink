from django.urls import path
from .views import ProductListAPIView, ProductDetailsAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsAPIView.as_view(), name='product-detail')
]