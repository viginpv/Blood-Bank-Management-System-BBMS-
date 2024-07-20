from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from django.contrib import messages
from hospital_app.models import BloodRequest, Hospital
from django.contrib.auth import logout

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

@login_required
def patient_profile(request):
    # Retrieve the patient associated with the logged-in user
    patient = Patient.objects.get(user=request.user)
    return render(request, 'patient_profile.html', {'patient': patient})

@login_required
def edit_patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        blood_group = request.POST.get('blood_group')

        patient.user.username = username
        patient.address = address
        patient.age = age
        patient.contact = contact
        patient.blood_group = blood_group

        patient.user.save()
        patient.save()
        
        return redirect('patient_profile')  # No need to pass patient_id
    return render(request, 'edit_patient_profile.html', {'patient': patient})

def submit_blood_request(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not logged in

    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        quantity = request.POST.get('quantity')
        hospital_id = request.POST.get('hospital')

        # Get the hospital object based on the provided ID
        try:
            hospital = Hospital.objects.get(id=hospital_id)
        except Hospital.DoesNotExist:
            return render(request, 'blood_request.html', {'error': 'Invalid hospital selected'})

        # Get the patient associated with the logged-in user
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            messages.error(request, "Patient profile does not exist.")
            return redirect('patient_dashboard')

        # Create a new blood request object
        new_request = BloodRequest.objects.create(
            patient=patient,
            hospital=hospital,
            blood_group=blood_group,
            quantity=quantity,
            status='pending'
        )
        return redirect('patient_dashboard')

    else:
        hospitals = Hospital.objects.all()
        return render(request, 'blood_request.html', {'hospitals': hospitals})

