from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.handleSignup, name="signup"),
    path("login", views.handleLogin, name="login"),
    path("logout", views.handleLogout, name="logout"),
    path("user-accounts/", views.useraccounts, name="user-accounts"),
    path("update-profile/", views.updateprofile, name="update-profile"),
    path("equipment-list/", views.equipmentList, name="equipment-list"),
    path("add-equipment/", views.addEquipment, name="add-equipment"),
    path("delete-equipment/<int:id>", views.deleteEquipment, name="delete-equipment"),
    path("edit-equipment/<int:id>", views.editEquipment, name="edit-equipment"),
    path("update-equipment/", views.updateEquipment, name="update-equipment"),
]