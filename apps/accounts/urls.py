from django.urls import path
from . import views

urlpatterns = [
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
]
