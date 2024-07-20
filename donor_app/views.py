from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hospital_app.models import BloodRequest
from .models import Donor
from django.contrib.auth.models import User

@login_required
def donor_dashboard(request):
    blood_requests = BloodRequest.objects.filter(status='pending')
    return render(request, 'donor_dashboard.html', {'blood_requests': blood_requests})

def donor_blood_requests(request):
    blood_requests = BloodRequest.objects.filter(status='pending')
    return render(request, 'donor_blood_requests.html', {'blood_requests': blood_requests})

def fulfill_request_by_donor(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    blood_request.status = 'fulfilled'
    blood_request.save()
    return redirect('donor_blood_requests')

@login_required
def donor_profile(request):
    donor = get_object_or_404(Donor, user=request.user)
    return render(request, 'donor_profile.html', {'donor': donor})
@login_required
def edit_donor_profile(request):
    donor = get_object_or_404(Donor, user=request.user)
    user = donor.user  # Retrieve User object associated with the donor

    if request.method == 'POST':
        # Retrieve data from POST request
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        blood_group = request.POST.get('blood_group')

        user.username = username
        user.save()

        # Update donor profile fields (Donor model)
        donor.address = address
        donor.age = age
        donor.contact = contact
        donor.blood_group = blood_group
        donor.save()

        return redirect('donor_profile')

    return render(request, 'edit_donor_profile.html', {'donor': donor})

def certificate(request):
    return render(request,'certificate.html')