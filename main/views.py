from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from main.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="main:signup")
def index(request):
    return render(request, "index.html")

def handleSignup(request):
    if request.method == "POST":
        fullname = request.POST.get("full-name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = fullname.split(" ")[0]
        if len(fullname.split(" ")) > 1:
            last_name = fullname.split(" ")[1]
        else:
            last_name = ""
        # check is user exists
        if User.objects.filter(email=email).exists():
            # messages.error(request, "Email already exists")
            return render(request, "signup.html", {"error": "Email already exists"})
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            UserProfile.objects.create(user=user)
            user = authenticate(username=email, password=password)
            login(request, user)

            # messages.success(request, "Account created successfully")
            return redirect("main:user-accounts")
        
    return render(request, "signup.html")


def handleLogout(request):
    logout(request)
    return redirect("main:signup")


def useraccounts(request):
    user = UserProfile.objects.get(user=request.user)  
    return render(request, "user-accounts.html", {"user": user})

def updateprofile(request):
    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        user.user.first_name = request.POST.get("first-name")
        user.user.last_name = request.POST.get("last-name")
        user.user.email = request.POST.get("email")
        if request.POST.get("admin-user") == "on":
            user.role = "Admin User"
        else:
            user.role = "Regular User"
        user.save()
        user.user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("main:user-accounts")
    return render(request, "update-profile.html")