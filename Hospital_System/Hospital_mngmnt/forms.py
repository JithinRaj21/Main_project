from django import forms

from .models import Appointment, Contact


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name','phone_number','email_id','doctor_name','booking_date']

        widgets = {
            'booking_date': DateInput(),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message'}),
        }

   