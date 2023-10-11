"""
doctor_appointment_system URL Configuration

"""

from django.urls import path
from appointment.views import *
from django.conf import settings
from django.conf.urls.static import static
from appointment import views

app_name = 'appointment'

urlpatterns = [

    # path('', HomePageView.as_view(), name='home'),
    path('service', ServiceView.as_view(), name='service'),
    path('doctor/appointment/create', AppointmentCreateView.as_view(), name='doctor-appointment-create'),
    path('doctor/appointment/', AppointmentListView.as_view(), name='doctor-appointment'),
    path('<pk>/delete/', AppointmentDeleteView.as_view(), name='delete-appointment'),
    path('<int:pk>/patient/delete/', views.delete_patient, name='delete-patient'),
    path('<int:pk>/doctor/delete/', views.delete_doctor, name='delete-doctor'),
    path('patient-take-appointment/', TakeAppointmentView.as_view(), name='take-appointment'),
    path('search/', SearchView.as_view(), name='search'),
    # path('search/', views.search, name='search'),
    path('patient/', views.patient_list, name='patient-list'),
    path('doctor-list/', views.doctor_list, name='doctor-list'),

    path('patients/<id>/', views.doctordetails, name='doctor-detail'),
    path('detail/<int:id>/', views.display_cart, name='detail'),
    path('doctordetail/<id>/', views.view_doctor_detail, name='docdetail'),
    path('patient/profile/update/<id>/', views.editprofile, name='patient-profile-update'),
    path('doctor/profile/update/<id>/', views.editprofiledoctor, name='doctor-profile-update'),
   # path('patient/profile/update/<id>/', EditPatientProfileView1.as_view(), name='patient-profile-update2'),
    path('payment/<int:id>', views.payment, name = 'payment'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
    # Generating Invoice
    path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    
    #path('patients/<int:appointment_id>', PatientPerAppointmentView.as_view(), name='patient-list'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
