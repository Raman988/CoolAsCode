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
    path('service', views.service_view,  name='service'),
    path('<int:pk>/patient/delete/', views.delete_patient, name='delete-patient'),
    path('<int:pk>/doctor/delete/', views.delete_doctor, name='delete-doctor'),
    path('search/', views.search_view, name='search'),
    path('patient/', views.patient_list, name='patient-list'),
    path('doctor-list/', views.doctor_list, name='doctor-list'),

    path('patients/<id>/', views.doctordetails, name='doctor-detail'),
    path('detail/<int:id>/', views.display_cart, name='detail'),
    path('doctordetail/<id>/', views.view_doctor_detail, name='docdetail'),
    path('patient/profile/update/<id>/', views.editprofile, name='patient-profile-update'),
    path('doctor/profile/update/<id>/', views.editprofiledoctor, name='doctor-profile-update'),
    path('payment/<int:id>', views.payment, name = 'payment'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
    path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
