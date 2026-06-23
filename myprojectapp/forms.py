from django import forms
from .models import PreOrder


class PreBookingForm(forms.ModelForm):

    class Meta:
        model = PreBooking
        fields = '__all__'