from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.get_laundry_categories, name='get_laundry_categories'),
    path('order/', views.create_laundry_invoice, name='create_laundry_invoice'),
]
