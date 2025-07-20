from django.urls import path
from . import views, admin_views

urlpatterns = [
    # Public endpoints
    path('items/', views.get_cds_items, name='get_cds_items'),
    path('items/<int:item_id>/', views.get_cds_item_detail, name='get_cds_item_detail'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    
    # CDS Owner endpoints
    path('admin/items/create/', admin_views.create_cds_item, name='create_cds_item'),
    path('admin/items/<int:item_id>/update/', admin_views.update_cds_item, name='update_cds_item'),
    path('admin/items/<int:item_id>/delete/', admin_views.delete_cds_item, name='delete_cds_item'),
    path('admin/analytics/', admin_views.get_cds_analytics, name='get_cds_analytics'),
]