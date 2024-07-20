from django.shortcuts import render, redirect, get_object_or_404
from .models import BloodRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from patient_app.models import Patient
from django.contrib import messages
from hospital_app.models import Hospital
from donor_app.models import Donor



def hospital_dashboard(request):
    return render(request, 'hospital_dashboard.html')

def hospital_blood_requests(request):
    blood_requests = BloodRequest.objects.filter(status='pending')
    return render(request, 'hospital_blood_requests.html', {'blood_requests': blood_requests})

def fulfill_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    blood_request.status = 'fulfilled'
    blood_request.save()
    return redirect('hospital_blood_requests')

@login_required
def add_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        blood_group = request.POST.get('blood_group')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_patient')

        
        user = User.objects.create_user(username=username, password=password)

        Patient.objects.create(
            user=user,
            address=address,
            age=age,
            contact=contact,
            blood_group=blood_group
        )

        messages.success(request, 'Patient added successfully.')
        return redirect('list_patients')  
    else:
        return render(request, 'add_patient.html')
    
@login_required
def list_patients(request):
    patients = Patient.objects.all()
    return render(request, 'list_patients.html', {'patients': patients})

def hospital_profile(request):
    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        messages.error(request, "Hospital profile does not exist.")
        return redirect('hospital_dashboard')  # Redirect to a safe page
    return render(request, 'hospital_profile.html', {'hospital': hospital})

@login_required
def edit_hospital_profile(request):
    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        messages.error(request, "Hospital profile does not exist.")
        return redirect('hospital_dashboard')

    if request.method == 'POST':
        # Process the form submission
        hospital_name = request.POST['hospital_name']
        address = request.POST['address']
        contact = request.POST['contact']

        # Update hospital details
        user = hospital.user
        user.username = hospital_name
        user.save()

        hospital.address = address
        hospital.contact = contact
        hospital.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('hospital_profile')
    else:
        return render(request, 'edit_hospital_profile.html', {'hospital': hospital})
    


@login_required
def submit_hospital_blood_request(request):
    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        quantity = request.POST.get('quantity')
        patient_id = request.POST.get('patient')

        # Get the patient object based on the provided ID
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return render(request, 'hospital_blood_request.html', {'error': 'Invalid patient selected'})

        # Get the hospital associated with the logged-in user
        try:
            hospital = Hospital.objects.get(user=request.user)
        except Hospital.DoesNotExist:
            messages.error(request, "Hospital profile does not exist.")
            return redirect('hospital_dashboard')

        # Create a new blood request object
        new_request = BloodRequest.objects.create(
            patient=patient,
            hospital=hospital,
            blood_group=blood_group,
            quantity=quantity,
            status='pending'
        )
        return redirect('hospital_dashboard')

    else:
        patients = Patient.objects.all()
        return render(request, 'hospital_blood_request.html', {'patients': patients})
  
#function for add delete and edit donor by hospital

@login_required
def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donor/donor_list.html', {'donors': donors})

@login_required
def add_donor_by_hospital(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        blood_group = request.POST.get('blood_group')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_donor_by_hospital')

        user = User.objects.create_user(username=username, password=password)

        Donor.objects.create(
            user=user,
            address=address,
            age=age,
            contact=contact,
            blood_group=blood_group
        )

        messages.success(request, 'Donor added successfully.')
        return redirect('donor_list')
    else:
        return render(request, 'donor/add_donor_hospital.html')

@login_required
def edit_donor_by_hospital(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    
    if request.method == 'POST':
        donor.user.username = request.POST.get('username')
        donor.user.set_password(request.POST.get('password'))  # Update the password
        donor.user.save()
        donor.address = request.POST.get('address')
        donor.age = request.POST.get('age')
        donor.contact = request.POST.get('contact')
        donor.blood_group = request.POST.get('blood_group')
        donor.save()

        messages.success(request, 'Donor details updated successfully.')
        return redirect('donor_list')
    else:
        return render(request, 'donor/edit_donor_hospital.html', {'donor': donor})

    
@login_required
def delete_donor_by_hospital(request, pk):
    donor = get_object_or_404(Donor, id=pk)
    user = donor.user
    donor.delete()
    user.delete()
    messages.success(request, 'Donor deleted successfully.')
    return redirect('donor_list')
