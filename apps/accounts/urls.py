from django.urls import path
from . import views, jwt_views
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    # JWT Authentication endpoints
    path("jwt/login/", jwt_views.jwt_login, name="jwt_login"),
    path("jwt/refresh/", jwt_views.CustomTokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path("jwt/logout/", jwt_views.logout_user, name="jwt_logout"),
    path("jwt/register/", jwt_views.register_user, name="jwt_register"),
    
    # User management endpoints (JWT)
    path("jwt/current-user/", jwt_views.get_current_user, name="jwt_current_user"),
    path("jwt/update-profile/", jwt_views.update_profile, name="jwt_update_profile"),
    path("jwt/check-permission/", jwt_views.check_permission, name="jwt_check_permission"),
    path("jwt/get-permissions/", jwt_views.get_user_permissions, name="jwt_get_permissions"),
    
    # CDS Owner endpoints (JWT)
    path("jwt/list-users/", jwt_views.list_users, name="jwt_list_users"),
    path("jwt/change-role/", jwt_views.change_user_role, name="jwt_change_role"),
    path("jwt/toggle-status/", jwt_views.toggle_user_status, name="jwt_toggle_status"),
    
    # Legacy session-based endpoints (for backward compatibility)
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("current-user/", views.get_current_user, name="current_user"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("csrf/", views.get_csrf_token, name="get_csrf_token"),
    
    # CDS Owner endpoints (session-based)
    path("list-users/", views.list_users, name="list_users"),
    path("change-role/", views.change_user_role, name="change_role"),
    path("toggle-status/", views.toggle_user_status, name="toggle_status"),
    path("check-permission/", views.check_permission, name="check_permission"),
    path("get-permissions/", views.get_user_permissions, name="get_permissions"),
]
