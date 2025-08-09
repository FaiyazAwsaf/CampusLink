from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("current-user/", views.get_current_user, name="current_user"),
    path("csrf/", views.get_csrf_token, name="get_csrf_token"),
]
