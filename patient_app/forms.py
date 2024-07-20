from django import forms
from hospital_app.models import BloodRequest

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['hospital', 'blood_group', 'quantity']
