
from django.urls import path
from . import views
from .views import user_cds_orders

urlpatterns = [
    # Public endpoints
    path('items/', views.get_cds_items, name='get_cds_items'),
    path('items/<int:item_id>/', views.get_cds_item_detail, name='get_cds_item_detail'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('categories/', views.get_cds_categories, name='get_cds_categories'),
    path('submit_order/', views.submit_cds_order, name='submit_cds_order'),
    path('user_orders/', user_cds_orders, name='user_cds_orders'),
    
    # CDS Owner management endpoints
    path('owner/items/', views.manage_cds_items, name='manage_cds_items'),
    path('owner/items/<int:item_id>/', views.manage_cds_item, name='manage_cds_item'),
    path('owner/orders/', views.get_all_cds_orders, name='get_all_cds_orders'),
    path('owner/orders/<int:order_id>/', views.get_cds_order_details_owner, name='get_cds_order_details_owner'),
    path('owner/orders/<int:order_id>/status/', views.update_cds_order_status, name='update_cds_order_status'),
    path('owner/orders/<int:order_id>/delete/', views.delete_cds_order, name='delete_cds_order'),
]