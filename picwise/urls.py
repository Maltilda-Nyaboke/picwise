from django.conf import settings
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login", views.login_user, name="login"),
    path("profile/", views.profile, name="profile"),
]
