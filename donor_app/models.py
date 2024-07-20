# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    age = models.PositiveIntegerField()
    contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=3)

    def __str__(self):
        return self.user.username
    

