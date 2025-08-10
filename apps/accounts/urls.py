from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from . import views
from . import jwt_views

urlpatterns = [
    # JWT Authentication endpoints
    path("auth/login/", jwt_views.LoginView.as_view(), name="jwt_login"),
    path("auth/logout/", jwt_views.logout_view, name="jwt_logout"),
    path("auth/register/", jwt_views.RegisterView.as_view(), name="jwt_register"),
    path("auth/refresh/", jwt_views.TokenRefreshView.as_view(), name="jwt_refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path("auth/current-user/", jwt_views.current_user_view, name="jwt_current_user"),
    path("auth/update-profile/", jwt_views.update_profile_view, name="jwt_update_profile"),
    path("auth/change-password/", jwt_views.change_password_view, name="jwt_change_password"),
    path("auth/verify-token/", jwt_views.verify_token_view, name="jwt_verify_token"),
    
    # Legacy endpoints (for backward compatibility)
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("current-user/", views.get_current_user, name="current_user"),
    path("user-role/", views.get_user_role, name="get_user_role"),
    path("permissions/", views.get_user_permissions, name="get_user_permissions"),
    path("check-permission/", views.check_permission, name="check_permission"),
    path("change-role/", views.change_user_role, name="change_user_role"),
    path("users/", views.list_users, name="list_users"),
    path("user-profile/", views.get_user_profile, name="get_user_profile"),
    path("user-profile/<int:user_id>/", views.get_user_profile, name="get_user_profile_by_id"),
    path("toggle-status/", views.toggle_user_status, name="toggle_user_status"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("csrf/", views.get_csrf_token, name="get_csrf_token"),
]
