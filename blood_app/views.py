from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from admin_app.models import Admin
from donor_app.models import Donor
from hospital_app.models import Hospital
from patient_app.models import Patient
from main_app.models import Main

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        address = request.POST['address']
        age = request.POST['age']
        contact = request.POST['contact']
        blood_group = request.POST['blood_group']
        user_type = request.POST['user_type']

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        if user_type == 'patient':
            Patient.objects.create(user=user, address=address, age=age, contact=contact, blood_group=blood_group)
        elif user_type == 'donor':
            Donor.objects.create(user=user, address=address, age=age, contact=contact, blood_group=blood_group)
        elif user_type == 'hospital':
            Hospital.objects.create(user=user, address=address, contact=contact)
        elif user_type == 'main':
            Main.objects.create(user=user, address=address, contact=contact)

        return redirect('login_view')  

    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'donor'):
                return redirect('donor_dashboard')
            elif hasattr(user, 'hospital'):
                return redirect('hospital_dashboard')
            elif hasattr(user, 'main'):
                return redirect('main_dashboard')
            else:
                return redirect('home')  # Redirect to home if user type is not matched
    return render(request, 'login.html')
