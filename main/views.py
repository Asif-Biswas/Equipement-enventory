from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from main.models import UserProfile, Equipment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize


# Create your views here.

@login_required(login_url="main:signup")
def index(request):
    return render(request, "index.html")

def handleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("main:index")
    return render(request, "login.html")

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

def equipmentList(request):
    equipments = Equipment.objects.all()
    context = {
        "equipments": equipments,
    }
    return render(request, "equipment-list.html", context)

def addEquipment(request):
    if request.method == "POST":
        name = request.POST.get("device-name")
        device_type = request.POST.get("device-type")
        quantity = request.POST.get("quantity")
        audit = request.POST.get("audit")
        location = request.POST.get("location")
        equipment = Equipment.objects.create(name=name, device_type=device_type, quantity=quantity, audit_date=audit, location=location)
        equipment.save()

        return redirect("main:equipment-list")

def deleteEquipment(request, id):
    equipment = Equipment.objects.get(id=id)
    equipment.delete()
    return redirect("main:equipment-list")

def editEquipment(request, id):
    equipment = Equipment.objects.get(id=id)
    equipment_json = serialize('json', [equipment])
    print(equipment_json)
    return JsonResponse(equipment_json, safe=False)

def updateEquipment(request):
    if request.method == "POST":
        id = request.POST.get("id")
        equipment = Equipment.objects.get(id=id)
        equipment.name = request.POST.get("device-name")
        equipment.device_type = request.POST.get("device-type")
        equipment.quantity = request.POST.get("quantity")
        equipment.audit_date = request.POST.get("audit")
        equipment.location = request.POST.get("location")
        equipment.save()
        return redirect("main:equipment-list")
    return render(request, "edit-equipment.html")