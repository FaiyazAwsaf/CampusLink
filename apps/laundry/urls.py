from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('categories/', views.get_laundry_categories, name='laundry_categories'),
    path('orders/create/', views.create_laundry_order, name='create_laundry_order'),
    path('orders/', views.get_user_orders, name='user_orders'),
    path('orders/<str:invoice_number>/', views.get_order_details, name='order_details'),
    
    # Staff management endpoints
    path('staff/categories/', views.manage_laundry_categories, name='manage_laundry_categories'),
    path('staff/categories/<int:category_id>/', views.manage_laundry_category, name='manage_laundry_category'),
    path('staff/orders/', views.get_all_orders, name='get_all_orders'),
    path('staff/orders/<int:order_id>/', views.get_order_details_staff, name='get_order_details_staff'),
    path('staff/orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('staff/orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
]