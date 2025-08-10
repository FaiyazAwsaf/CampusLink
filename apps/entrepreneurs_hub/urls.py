from django.urls import path
from .views import *

urlpatterns = [
    # Public endpoints
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsAPIView.as_view(), name='product-detail'),
    path('products/storefront_name/', StorefrontAPIView.as_view(), name='storefront-names'),
    path('products/storefronts/', StorefrontsAPIView.as_view(), name='storefront-list'),
    path('products/categories/', ProductCategoryAPIView.as_view(), name='product-categories'),
    path('products/recent/', RecentlyAddedProducts.as_view(), name='recent-products'),
    
    # Entrepreneur endpoints
    path('entrepreneur/storefronts/create/', create_storefront, name='create_storefront'),
    path('entrepreneur/storefronts/', get_my_storefronts, name='my_storefronts'),
    path('entrepreneur/products/', get_my_products, name='my_products'),
    path('entrepreneur/products/create/', create_product, name='create_product'),
    path('entrepreneur/products/<int:product_id>/update/', update_product, name='update_product'),
    path('entrepreneur/products/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('entrepreneur/analytics/', get_entrepreneur_analytics, name='entrepreneur_analytics'),

    #Search
    path('search/', SearchViewAPI.as_view(), name='search-query')
]