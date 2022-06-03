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
    path('<pk>/patient/delete', PatientDeleteView.as_view(), name='delete-patient'),
    path('patient-take-appointment/<pk>', TakeAppointmentView.as_view(), name='take-appointment'),
    path('search/', SearchView.as_view(), name='search'),
    # path('search/', views.search, name='search'),
    path('patient/', PatientListView.as_view(), name='patient-list'),
    path('patients/<id>/', views.doctordetails, name='doctor-detail'),
    path('detail/', views.DisplayCart.as_view(), name='detail'),
    path('patient/profile/update/<id>/', views.editprofile, name='patient-profile-update'),
    path('doctor/profile/update/<id>/', views.editprofiledoctor, name='doctor-profile-update'),
   # path('patient/profile/update/<id>/', EditPatientProfileView1.as_view(), name='patient-profile-update2'),
    path('payment/', views.payment, name = 'payment'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
    # Generating Invoice
    path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),

    #path('patients/<int:appointment_id>', PatientPerAppointmentView.as_view(), name='patient-list'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
