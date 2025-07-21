from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsAPIView.as_view(), name='product-detail'),
    path('products/storefront_name/', StorefrontAPIView.as_view(), name='storefront-names'),
    path('products/storefronts/', StorefrontsAPIView.as_view(), name='storefront-list'),
    path('products/categories/', ProductCategoryAPIView.as_view(), name='product-categories'),
    path('products/recent/', RecentlyAddedProducts.as_view(), name='recent-products'),
    path('search/', SearchViewAPI.as_view(), name='search-query')
]