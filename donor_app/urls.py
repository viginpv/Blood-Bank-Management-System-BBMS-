from django.urls import path
from . import views

urlpatterns = [
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donor_blood_requests/', views.donor_blood_requests, name='donor_blood_requests'),
    path('fulfill_request/<int:request_id>/', views.fulfill_request_by_donor, name='fulfill_request_by_donor'),
    path('donor_profile/', views.donor_profile, name='donor_profile'),
    path('edit_donor_profile/', views.edit_donor_profile, name='edit_donor_profile'),
    path('certificate/', views.certificate, name='certificate'),
]
