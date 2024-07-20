from django.db import models
from patient_app.models import Patient
from django.utils import timezone
from django.contrib.auth.models import User

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.patient.user.username} - {self.blood_group} - {self.status}'
