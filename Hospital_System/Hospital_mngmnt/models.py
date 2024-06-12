from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=25)
    specialization = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media', default='', blank=True)
    availability = models.BooleanField(default=True)
    desc = models.CharField(max_length=250, default='')

    def __str__(self):
        return '{}'.format(self.name)


class Department(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='media', blank=True, default='')

    def __str__(self):
        return '{}'.format(self.name)


class Appointment(models.Model):
    patient_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    email_id = models.EmailField()
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='')


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(default='No message provided')
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100, default='')
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return '{}'.format(self.medication)


class Patient(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class MedicalRecord(models.Model):
    patient_name = models.CharField(max_length=50)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.patient_name)





class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Bill {self.id} - {self.patient.name}'
    

class Staff(models.Model):
    ROLE_CHOICES = [
        ('receptionist', 'Receptionist'),
        ('nurse', 'Nurse'),
        # Add other roles as needed
    ]
    
    name = models.CharField(max_length=100)
    phone_number =models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name   