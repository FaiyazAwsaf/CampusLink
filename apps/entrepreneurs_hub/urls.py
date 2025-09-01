from django.urls import path
from .views import *
from .advanced_search import (
    AdvancedSearchView,
    AutocompleteView,
    SearchSuggestionsView
)

from rest_framework.routers import DefaultRouter
from .views import ProductCRUDViewSet, StorefrontViewSet


urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductDetailsAPIView.as_view(), name='product-detail'),
    path('products/<int:product_id>/ratings/', ProductRatingsAPIView.as_view(), name='product-ratings'),
    path('products/<int:product_id>/rate/', SubmitRatingAPIView.as_view(), name='submit-rating'),
    path('products/storefront_name/', StorefrontAPIView.as_view(), name='storefront-names'),
    path('products/storefronts/', StorefrontsAPIView.as_view(), name='storefront-list'),
    path('products/categories/', ProductCategoryAPIView.as_view(), name='product-categories'),
    path('products/recent/', RecentlyAddedProducts.as_view(), name='recent-products'),
    path('search/', SearchViewAPI.as_view(), name='search-query'),
    path('search/advanced/', AdvancedSearchView.as_view(), name='advanced-search'),
    path('search/autocomplete/', AutocompleteView.as_view(), name='autocomplete'),
    path('search/suggestions/', SearchSuggestionsView.as_view(), name='search-suggestions'),
    ]

router = DefaultRouter()
router.register(r'products/manage', ProductCRUDViewSet, basename='product-crud')
router.register(r'storefronts', StorefrontViewSet, basename='storefront-crud')

urlpatterns += router.urls
