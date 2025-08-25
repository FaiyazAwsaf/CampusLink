
from django.urls import path
from . import views
from .views import user_cds_orders

urlpatterns = [
    path('items/', views.get_cds_items, name='get_cds_items'),
    path('items/<int:item_id>/', views.get_cds_item_detail, name='get_cds_item_detail'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('categories/', views.get_cds_categories, name='get_cds_categories'),
    path('submit_order/', views.submit_cds_order, name='submit_cds_order'),
    path('user_orders/', user_cds_orders, name='user_cds_orders'),
]