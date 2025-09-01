from django.urls import path
from .views import *
from .advanced_search import (
    AdvancedSearchView,
    AutocompleteView,
    SearchSuggestionsView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductDetailsAPIView.as_view(), name='product-detail'),
    path('products/<int:product_id>/ratings/', ProductRatingsAPIView.as_view(), name='product-ratings'),
    path('products/<int:product_id>/rate/', SubmitRatingAPIView.as_view(), name='submit-rating'),
    path('products/storefront_name/', StorefrontAPIView.as_view(), name='storefront-names'),
    path('products/storefronts/', StorefrontsAPIView.as_view(), name='storefront-list'),
    path('storefronts/<int:store_id>/', StorefrontDetailAPIView.as_view(), name='storefront-detail'),
    path('storefronts/<int:store_id>/products/', StorefrontProductsAPIView.as_view(), name='storefront-products'),
    path('products/categories/', ProductCategoryAPIView.as_view(), name='product-categories'),
    path('products/recent/', RecentlyAddedProducts.as_view(), name='recent-products'),
    path('search/', SearchViewAPI.as_view(), name='search-query'),
    path('search/advanced/', AdvancedSearchView.as_view(), name='advanced-search'),
    path('search/autocomplete/', AutocompleteView.as_view(), name='autocomplete'),
    path('search/suggestions/', SearchSuggestionsView.as_view(), name='search-suggestions'),
]
