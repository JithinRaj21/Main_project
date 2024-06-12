from django.urls import path
from .import views

urlpatterns = [
    path('',views.base,name='home'),

    path('doctor', views.doctor, name='doctor'),
    path('doctor_details/<pk>',views.doctor_detail,name='detail_doctor'),

    path('appointment/', views.appointment, name='appointment'),

    

    path('signout/',views.signout,name='logout'),

    path('contact',views.contact,name='contact'),
    path('contact_message',views.contact_success,name='contact_success'),

    # path('about', views.about, name='about'),
    path('department', views.department, name='department'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('appointment_cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('appointment_reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('patient_details/<str:patient_name>/', views.patient_details, name='patient_details'),


    path('doctor_register/', views.doctor_register, name='doctor_register'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_dashboard/<str:doctor_name>/', views.doctor_dashboard, name='doctor_dashboard'),
    path('edit_prescription/<int:appointment_id>/', views.edit_prescription, name='edit_prescription'),
    path('doctor_profile/<str:doctor_name>/', views.doctor_profile, name='doctor_profile'),


   # path('appointments_book/<str:doctor_name>/', views.appointment_for_doctor, name='appointment_for_doctor'),

    path('doctor/<int:doctor_id>/book_appointment/', views.book_appointment, name='book_appointment'),


    path('staff_register/', views.register_staff, name='register_staff'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('nurse/dashboard/', views.nurse_dashboard, name='nurse_dashboard'),

    path('view_patient_details/<int:patient_id>/',views.view_patient_details, name='patient_details'),
    path('view_patient_details_nurse/<int:patient_id>/',views.view_patient_details_nurse, name='patient_details_nurse'),

    path('receptionist/create_patient/', views.create_patient, name='create_patient'),
    path('receptionist/create_doctor/', views.create_doctor, name='create_doctor'),

    path('receptionist/generate_bill/', views.generate_bill, name='generate_bill'),
    path('view_bill/', views.view_bill, name='view_bill'),

    path('view_doctors/', views.view_doctors, name='view_doctors'),
    path('view_patients/', views.view_patients, name='view_patients'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),

    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    path('view_appointments/', views.view_appointments, name='view_appointments'),

    path('medical_record/<int:record_id>/', views.medical_record_details, name='medical_record_details'),
]

