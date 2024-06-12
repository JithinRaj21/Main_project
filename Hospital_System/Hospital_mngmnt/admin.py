from django.contrib import admin

from .models import Doctor, Department, Patient, MedicalRecord
from .models import Prescription, Appointment, Contact, Staff, Bill

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(Prescription)
admin.site.register(Patient)
admin.site.register(MedicalRecord)
admin.site.register(Staff)
admin.site.register(Bill)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'phone_number', 'email_id', 'doctor_name', 'booking_date', 'booked_on', 'status')


admin.site.register(Appointment, AppointmentAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')


admin.site.register(Contact, ContactAdmin)
