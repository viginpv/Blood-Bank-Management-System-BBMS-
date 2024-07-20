from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from patient_app.models import Patient
from django.contrib import messages
from django.contrib.auth.models import User
from hospital_app.models import Hospital
from donor_app.models import Donor


@login_required
def main_dashboard(request):
    context = {
        'username': request.user.username
    }
    return render(request, 'main_dashboard.html', context)

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, id):
    patient = get_object_or_404(Patient, id=id)
    context = {
        'patient': patient
    }
    return render(request, 'patient/patient_detail.html', context)

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
        
        return redirect('patient_list')  # Redirect to the patient list page after saving changes
    return render(request, 'patient/edit_patient.html', {'patient': patient})



@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patient_list')  # Replace with the name of your patient list view
    return redirect('patient_list')

@login_required
def add_patient_by_main(request):
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
        return redirect('main_dashboard')  
    else:
        return render(request, 'patient/add_patient_main.html')
    


    #view hopitals /edit/delete

@login_required
def hospital_list(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospital/hospital_list.html', {'hospitals': hospitals})

@login_required
def edit_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        hospital.name = request.POST.get('name', hospital.name)
        hospital.address = request.POST.get('address', hospital.address)
        hospital.contact = request.POST.get('contact', hospital.contact)
        hospital.save()
        messages.success(request, 'Hospital details updated successfully.')
        return redirect('hospital_list')
    return render(request, 'hospital/edit_hospital.html', {'hospital': hospital})

@login_required
def delete_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        hospital.delete()
        messages.success(request, 'Hospital deleted successfully.')
        return redirect('hospital_list')
    return render(request, 'hospital/confirm_delete.html', {'hospital': hospital})

#add hospital by main


@login_required
def add_hospital_by_main(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_hospital_by_main')

        user = User.objects.create_user(username=username, password=password)

        Hospital.objects.create(
            user=user,
            # name=name,
            address=address,
            contact=contact
        )

        messages.success(request, 'Hospital added successfully.')
        return redirect('hospital_list')  
    else:
        return render(request, 'hospital/add_hospital_main.html')
    

    # donor edit delete and show


@login_required
def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donor/donor_list.html', {'donors': donors})

@login_required
def add_donor_by_main(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        blood_group = request.POST.get('blood_group')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_donor_by_main')

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
        return render(request, 'donor/add_donor_main.html')

@login_required
def edit_donor_by_main(request, pk):
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
        return render(request, 'donor/edit_donor_main.html', {'donor': donor})

    
@login_required
def delete_donor_by_main(request, pk):
    donor = get_object_or_404(Donor, id=pk)
    user = donor.user
    donor.delete()
    user.delete()
    messages.success(request, 'Donor deleted successfully.')
    return redirect('donor_list')


###certificate generation

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

@login_required
def generate_certificate(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)

    # Create a HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{donor.user.username}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Draw the certificate content
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2.0, height - 100, "Certificate of Appreciation")

    p.setFont("Helvetica", 16)
    p.drawCentredString(width / 2.0, height - 150, f"This certificate is awarded to {donor.user.username}")

    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2.0, height - 200, "For their valuable contribution as a donor.")

    # Signature or other content can be added here
    p.setFont("Helvetica-Oblique", 12)
    p.drawCentredString(width / 2.0, height - 300, "Thank you for your support!")

    # Finish up
    p.showPage()
    p.save()

    return response

