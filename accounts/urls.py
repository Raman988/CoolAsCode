from django.urls import path
from .import  views
from appointment.views import *

from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
# from accounts.views import *
app_name = 'accounts'

urlpatterns=[
     path('register/',views.register, name='register'),
     path('Patient_register/',views.Patient_register.as_view(), name='Patient_register'),
     path('Doctor_register/',views.Doctor_register.as_view(), name='Doctor_register'),
     path('login/',views.LoginViewUser.as_view(), name='login'),
     path('',views.HomePageView.as_view(), name='index'),   
   #   path('logout/',views.LogoutViewUser.as_view(), name='logout'),
     path('logout/',views.logout_view, name='logout'),
     path('activate/<uidb64>/<token>', views.activate, name='activate'),
      #Forgot password
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "registration/password_reset_form.html", success_url = reverse_lazy("password_reset_complete")), 
     name="password_reset_confirm"),  # 3
     path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "registration/password_reset.html", success_url = reverse_lazy("password_reset_done"), email_template_name = 'registration/forgot_password_email.html'), 
     name="reset_password"),     # 1
     path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "registration/password_reset_sent.html"), 
     name="password_reset_done"),    # 2
     
     path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_reset_done.html"), 
     name="password_reset_complete"),   # 4
     # change password
     path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

     path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url = reverse_lazy("password_change_done")), 
        name='password_change'),
   #   path('patient/profile/update/', EditPatientProfileView.as_view(), name='patient-profile-update'),
   #   path('patient/profile/update/<id>/', EditPatientProfileView1.as_view(), name='patient-profile-update2'),
   #   path('doctor/profile/update/', EditDoctorProfileView.as_view(), name='doctor-profile-update'),



]