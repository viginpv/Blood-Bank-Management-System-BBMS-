from django.urls import path
from . import views

urlpatterns = [
    path('main_dashboard', views.main_dashboard, name='main_dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patient/<int:id>/', views.patient_detail, name='patient_detail'),
    path('edit_patient/<int:patient_id>/', views.edit_patient_profile, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('add_patient_by_main',views.add_patient_by_main,name='add_patient_by_main'),

    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospitals/edit/<int:hospital_id>/', views.edit_hospital, name='edit_hospital'),
    path('hospitals/delete/<int:hospital_id>/', views.delete_hospital, name='delete_hospital'),
    path('hospitals/add/', views.add_hospital_by_main, name='add_hospital_by_main'),

    path('donors/', views.donor_list, name='donor_list'),
    path('donors/add/', views.add_donor_by_main, name='add_donor_by_main'),
    path('donors/<int:pk>/edit/', views.edit_donor_by_main, name='edit_donor_by_main'),
    path('donors/<int:pk>/delete/', views.delete_donor_by_main, name='delete_donor_by_main'),

    path('donors/<int:donor_id>/certificate/', views.generate_certificate, name='generate_certificate'),
]
