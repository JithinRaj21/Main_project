from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import AppointmentForm, ContactForm
from .models import Department, Doctor, Appointment, Patient, Prescription, Staff, MedicalRecord



def base(request):
    department = Department.objects.all()
    doctor = Doctor.objects.all()

    context = {
        'department': department,
        'doctor': doctor,
    }

    return render(request, 'base.html', context)



def department(request):
    page = 1
    if request.GET:
        page = request.GET.get('page', 1)
    department_list = Department.objects.all()
    department_paginator = Paginator(department_list, 4)
    department_list = department_paginator.get_page(page)
    return render(request, 'department.html', {'department': department_list})



def doctor(request):
    page = 1
    if request.GET:
        page = request.GET.get('page', 1)
    doctor_list = Doctor.objects.all()
    doctor_paginator = Paginator(doctor_list, 4)
    doctor_list = doctor_paginator.get_page(page)
    return render(request, 'doctor.html', {'doctor': doctor_list})



def doctor_detail(request, pk):
    doctors = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor_detail.html', {'doctors': doctors})




def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'message.html')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})



def contact_success(request):
    return render(request, 'message.html')



def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'login.html', {'error': 'Passwords do not match'})

        if Patient.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'Email already exists'})

        patient = Patient(
            name=name,
            phone_number=phone_number,
            email=email,
            password=make_password(password)  
        )
        patient.save()
        messages.success(request, 'Registration Successful,you can now Login !.')
        return redirect('login')
    return render(request, 'login.html')




def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            patient = Patient.objects.get(email=email)
            if check_password(password, patient.password):
                # Create a session
                request.session['patient_id'] = patient.id

                messages.success(request, 'Login Successful!')
                return redirect('patient_dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except Patient.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')




def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return redirect('login')

    appointments = Appointment.objects.filter(patient_name=patient.name)
    prescriptions = Prescription.objects.filter(patient_name=patient.name)

    context = {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
    }
    return render(request, 'patient_dashboard.html', context)




def cancel_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = 'cancelled'
        appointment.save()
        return redirect('patient_dashboard')
    else:
        
        return redirect('patient_dashboard')




def reschedule_appointment(request, appointment_id):
    if request.method == 'POST':
        new_date = request.POST.get('new_date')
        if new_date:
            appointment = get_object_or_404(Appointment, id=appointment_id)
            appointment.booking_date = new_date
            if appointment.status == 'cancelled':
                appointment.status = 'confirmed'
            appointment.save()
            return redirect('patient_dashboard')




def patient_details(request, patient_name):
    patient = get_object_or_404(Patient, name=patient_name)
    appointments = Appointment.objects.filter(patient_name=patient_name)
    prescriptions = Prescription.objects.filter(patient_name=patient_name)
    return render(request, 'patient_details.html', {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
    })




def signout(request):
    logout(request)
    return redirect('home')



def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'appointment_success.html')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})



def doctor_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        password = request.POST.get('password')

        
        try:
            doctor = Doctor.objects.get(name=name)
           
            user, created = User.objects.get_or_create(username=name)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password set successfully. You can now login.')
            
            return redirect('doctor_login')
        except Doctor.DoesNotExist:
            messages.error(request, 'No doctor found with the provided name.')
            return render(request, 'doctor_login.html')

    return render(request, 'doctor_login.html')



def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(name=username)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.username == username:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.')
                    return redirect(reverse('doctor_dashboard', kwargs={
                        'doctor_name': username}))  
                else:
                    messages.error(request, 'You are not authorized to login here.')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        except Doctor.DoesNotExist:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'doctor_login.html')




def doctor_dashboard(request, doctor_name):
    try:
       
        doctor = Doctor.objects.get(name=doctor_name)

        appointments = Appointment.objects.filter(doctor_name=doctor, status='confirmed')

        prescriptions = Prescription.objects.filter(doctor=doctor)
        patients_with_confirmed_appointments = [appointment.patient_name for appointment in appointments]
       
        medical_records = MedicalRecord.objects.filter(doctor=doctor,patient_name__in=patients_with_confirmed_appointments)

       
        return render(request, 'doctor_dashboard.html', {
            'doctor': doctor,
            'appointments': appointments,
            'prescriptions': prescriptions,
            'medical_records': medical_records
        })
    except Doctor.DoesNotExist:
        
        return redirect('doctor_login')



def edit_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    prescription, created = Prescription.objects.get_or_create(
        doctor=appointment.doctor_name,
        patient_name=appointment.patient_name,
        start_date=appointment.booking_date,
        
        defaults={
            'medication': '',
            'dosage': '',
            'frequency': '',
            'end_date': appointment.booking_date, 
            'notes': '',
        }
    )

    if request.method == 'POST':
        medication = request.POST.get('medication')
        dosage = request.POST.get('dosage')
        frequency = request.POST.get('frequency')
        notes = request.POST.get('notes')

        prescription.medication = medication
        prescription.dosage = dosage
        prescription.frequency = frequency
        prescription.notes = notes
        prescription.save()

        return redirect(reverse('doctor_dashboard', kwargs={'doctor_name': appointment.doctor_name.name}))

    context = {
        'appointment': appointment,
        'prescription': prescription
    }
    return render(request, 'doctor_dashboard.html', context)



@login_required
def doctor_profile(request, doctor_name):
    doctor = get_object_or_404(Doctor, name=doctor_name)
    doctor_username = request.user.username
    return render(request, 'doctor_profile.html', {'doctor': doctor, 'doctor_username': doctor_username})



def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    return render(request, 'doctor_appointment.html', {'doctor': doctor})



def register_staff(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        role = request.POST['role']
        Staff.objects.create(name=name, email=email, password=password, role=role)
        return redirect('staff_login')
    return render(request, 'register_staff.html')



def staff_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        staff = Staff.objects.filter(email=email).first()
        if staff and check_password(password, staff.password):
            # Set session or token here
            request.session['staff_id'] = staff.id
            request.session['staff_role'] = staff.role
            
            if staff.role == 'receptionist':
                return redirect('receptionist_dashboard')
            elif staff.role == 'nurse':
                return redirect('nurse_dashboard')
        else:
           
            pass
    return render(request, 'staff_login.html')



def receptionist_dashboard(request):
    if request.session.get('staff_role') != 'receptionist':
        return redirect('login')
    
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('login')

    staff = Staff.objects.get(id=staff_id)
    
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()
    medical_records = MedicalRecord.objects.all()
    total_doctors = Doctor.objects.count() 
    total_patients = patients.count()       
    total_appointments = appointments.count()  
    
    context = {
        'staff_name': staff.name,
        'patients': patients,
        'medical_records':medical_records,
        'appointments': appointments,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
    }
    return render(request, 'receptionist_dashboard.html', context)



def nurse_dashboard(request):
    if request.session.get('staff_role') != 'nurse':
        return redirect('login')
    
    staff_id = request.session.get('staff_id')
    staff = Staff.objects.get(id=staff_id)
    
    patients = Patient.objects.all()
    medical_records = MedicalRecord.objects.all()
    context = {
        'staff_name': staff.name,
        'patients': patients,
        'medical_records': medical_records,
    }
    return render(request, 'nurse_dashboard.html', context)
    

  
def view_doctors(request):
    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors
    }
    return render(request, 'view_doctors.html', context)    



def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect(reverse('view_doctors'))



def view_patients(request):
    patients = Patient.objects.all()
    context = {
        'patients': patients
    }
    return render(request, 'view_patients.html', context)



def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect(reverse('view_patients'))




def view_patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient_name=patient.name)
    prescriptions = Prescription.objects.filter(patient_name=patient.name)
    context = {
        'patient': patient,
        'appointments':appointments,
        'prescriptions': prescriptions
    }
    return render(request, 'view_patient_details.html', context)




def view_patient_details_nurse(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
   
    prescriptions = Prescription.objects.filter(patient_name=patient.name)
    context = {
        'patient': patient,
        
        'prescriptions': prescriptions
    }
    return render(request, 'view_patient_details_nurse.html', context)




def create_patient(request):
    if request.session.get('staff_role') != 'receptionist':
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
      
        Patient.objects.create(name=name, phone_number=phone_number, email=email)
        return redirect('receptionist_dashboard')
    
    return render(request, 'create_patient.html')




def create_doctor(request):
    if request.session.get('staff_role') != 'receptionist':
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST['name']
        specialization = request.POST['specialization']
        image = request.FILES['image']
        desc = request.POST['desc']
        availability = request.POST.get('availability') == 'on'
        Doctor.objects.create(name=name, specialization=specialization, image=image, desc=desc, availability=availability)
        return redirect('receptionist_dashboard')
    
    return render(request, 'create_doctor.html')



def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'view_appointments.html', {'appointments': appointments})




def generate_bill(request):
    if request.session.get('staff_role') != 'receptionist':
        return redirect('login')
    
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        date_issued = request.POST.get('date_issued')
        charge_descriptions = request.POST.getlist('charge_description[]')
        charge_amounts = request.POST.getlist('charge_amount[]')

        itemized_charges = []
        total_amount = 0
        
        for description, amount in zip(charge_descriptions, charge_amounts):
            amount = float(amount)
            itemized_charges.append({'description': description, 'amount': amount})
            total_amount += amount
        
        request.session['bill'] = {
            'patient_name': Patient.objects.get(id=patient_id).name,
            'patient_id': patient_id,
            'date_issued': date_issued,
            'itemized_charges': itemized_charges,
            'total_amount': total_amount,
        }
        
        return redirect('view_bill')
    
    patients = Patient.objects.all()
    return render(request, 'generate_bill.html', {'patients': patients})





def view_bill(request):
    bill = request.session.get('bill')
    if not bill:
        return redirect('generate_bill')
    return render(request, 'bill.html', bill)




def medical_record_details(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    return render(request, 'medical_details.html', {'record': record})






  

