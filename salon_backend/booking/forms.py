from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'service', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
