from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('hospital_dashboard',views.hospital_dashboard,name='hospital_dashboard'),
    path('requests/', views.hospital_blood_requests, name='hospital_blood_requests'),
    path('hospital/fulfill/<int:request_id>/', views.fulfill_request, name='fulfill_request'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('list_patients/', views.list_patients, name='list_patients'),
    path('submit_hospital_blood_request/', views.submit_hospital_blood_request, name='submit_hospital_blood_request'),
    path('edit_hospital_profile/', views.edit_hospital_profile, name='edit_hospital_profile'),
    path('hospital_profile/', views.hospital_profile, name='hospital_profile'),

    path('donors/', views.donor_list, name='donor_list'),
    path('donors/add/', views.add_donor_by_hospital, name='add_donor_by_main'),
    path('donors/<int:pk>/edit/', views.edit_donor_by_hospital, name='edit_donor_by_main'),
    path('donors/<int:pk>/delete/', views.delete_donor_by_hospital, name='delete_donor_by_main'),
    
]
