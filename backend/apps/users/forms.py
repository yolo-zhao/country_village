from django import forms
from django.contrib.auth.models import User
from .models import TouristProfile, FarmerProfile

class TouristProfileForm(forms.ModelForm):
    class Meta:
        model = TouristProfile
        fields = ['nickname', 'contact_phone']

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['farm_name', 'contact_phone']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']