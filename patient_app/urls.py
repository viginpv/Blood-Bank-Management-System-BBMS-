from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('patient_profile/',views.patient_profile,name='patient_profile'),
    path('patient/<int:patient_id>/', views.edit_patient_profile, name='edit_patient_profile'),
    path('submit_blood_request/', views.submit_blood_request, name='submit_blood_request'),

]
