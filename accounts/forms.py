from django import forms
from django.contrib.auth.models import User
from .models import AgentCode

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    admin_code = forms.CharField(max_length=30,required = False)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = AgentCode
        fields = ('code', 'approved')
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['pickup_location', 'dropoff_location', 'date', 'vehicle_name', 'model_no', 'pax', 'capacity', 'description', 'price']