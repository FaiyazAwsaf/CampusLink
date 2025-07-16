from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('current-user/', views.get_current_user, name='current_user'),
    
    # Authorization endpoints
    path('check-permission/', views.check_permission, name='check_permission'),
    path('permissions/', views.get_user_permissions, name='user_permissions'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # Admin endpoints
    path('admin/users/', views.list_users, name='list_users'),
    path('admin/users/change-role/', views.change_user_role, name='change_user_role'),
    path('admin/users/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
]