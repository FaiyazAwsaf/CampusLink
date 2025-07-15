from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.get_laundry_categories, name='laundry_categories'),
    path('orders/create/', views.create_laundry_order, name='create_laundry_order'),
    path('orders/', views.get_user_orders, name='user_orders'),
    path('orders/<str:invoice_number>/', views.get_order_details, name='order_details'),
]