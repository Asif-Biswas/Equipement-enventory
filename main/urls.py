from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.handleSignup, name="signup"),
    path("logout", views.handleLogout, name="logout"),
    path("user-accounts/", views.useraccounts, name="user-accounts"),
    path("update-profile/", views.updateprofile, name="update-profile"),
]