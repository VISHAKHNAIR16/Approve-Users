# forms.py
from django import forms

class TransferSearchForm(forms.Form):
    pickup_location = forms.CharField(label='Pickup Location', max_length=100)
    dropoff_location = forms.CharField(label='Dropoff Location', max_length=100)
    date = forms.DateField(widget=forms.SelectDateWidget())
    num_people = forms.IntegerField(label='Number of People', min_value=1)
