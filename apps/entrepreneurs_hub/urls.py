from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsAPIView.as_view(), name='product-detail'),
    path('products/storefronts/', StorefrontAPIView.as_view(), name='storefront-list'),
    path('products/categories/', ProductCategoryAPIView.as_view(), name='product-categories'),
    path('products/recent/', RecentlyAddedProducts.as_view(), name='recent-products'),
]