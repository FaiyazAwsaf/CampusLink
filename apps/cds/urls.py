from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.get_cds_items, name='get_cds_items'),
]