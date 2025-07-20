from django.urls import path
from . import views

urlpatterns = [
    # Public/Customer endpoints
    path('categories/', views.get_laundry_categories, name='laundry_categories'),
    path('orders/create/', views.create_laundry_order, name='create_laundry_order'),
    path('orders/', views.get_user_orders, name='user_orders'),
    path('orders/<str:invoice_number>/', views.get_order_details, name='order_details'),
    
    # Laundry Staff endpoints
    path('staff/orders/', views.get_all_laundry_orders, name='staff_all_orders'),
    path('staff/orders/<str:invoice_number>/status/', views.update_order_status, name='update_order_status'),
    path('staff/orders/<str:invoice_number>/', views.get_order_details_staff, name='staff_order_details'),
    path('staff/analytics/', views.get_laundry_analytics, name='laundry_analytics'),
]