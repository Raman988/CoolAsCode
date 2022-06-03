from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from django.views.generic import CreateView,ListView
from .form import PatientSignUpForm, DoctorSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Doctor, DoctorAdditional, PatientAdditional
# from .models import User
from django.contrib.auth.views import LoginView, LogoutView

from docmed import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from appointment.models import Appointment
def register(request):
    return render(request, 'register.html')

class Patient_register(CreateView,SuccessMessageMixin):
    # model = CustomUser
    form_class = PatientSignUpForm
    template_name = 'Patient_register.html'
    success_url = reverse_lazy('accounts:Patient_register')
    # success_message = "Redirect successfully created!"


    def post(self, request, *args, **kwargs):
        # form = PatientSignUpForm(request.POST)
        user_email = request.POST.get('email')
        try:
            existing_user = CustomUser.objects.get(email = user_email)
            if(existing_user.is_active == False):
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            age = request.POST.get('age')
            # gender = request.POST.get('gender')
            user = CustomUser.objects.get(email = user_email)
            s_add = PatientAdditional.objects.create(user = user, age = age)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)     #www.Docmed.in:8000  127.0.0.1:8000 
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #print(message)
            to_email = user_email   
            form = PatientSignUpForm(request.POST)   # here we are again calling all its validations
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list= [to_email],
                    fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
                )
                messages.success(request, "link has been sent to your email id. please check your inbox and if its not there check your spam as well.")
                return self.render_to_response({'form':form})
            except:
                form.add_error('', 'Error Occured In Sending Mail, Try Again')
                messages.error(request, "Error Occured In Sending Mail, Try Again")
                return self.render_to_response({'form':form})
        else:
            return response
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('/')
# template_name = 'firstapp/registerbasicuser.html'
#     form_class = RegistrationForm
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        login(request, user)
        messages.success(request, "Successfully Logged In")
        return redirect(reverse_lazy('index'))
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')    


class Doctor_register(CreateView):
    model = CustomUser
    form_class = DoctorSignUpForm
    template_name = 'Doctor_register.html'
    success_url = reverse_lazy('accounts:Doctor_register')

    def post(self, request, *args, **kwargs):
        #form = RegistrationForm(request.POST)
        user_email = request.POST.get('email')
        try:
            existing_user = CustomUser.objects.get(email = user_email)
            if(existing_user.is_active == False):
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            location = request.POST.get('location')
            your_expertise = request.POST.get('your_expertise')
            # gender = request.POST.get('gender')

            user = CustomUser.objects.get(email = user_email)
            d_add = DoctorAdditional.objects.create(user = user, location = location, your_expertise=your_expertise)

            user.is_active = False
            user.save()
            current_site = get_current_site(request)     #www.Docmed.in:8000  127.0.0.1:8000 
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #print(message)
            to_email = user_email   
            form = DoctorSignUpForm(request.POST)   # here we are again calling all its validations
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list= [to_email],
                    fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
                )
                messages.success(request, "link has been sent to your email id. please check your inbox and if its not there check your spam as well.")
                return self.render_to_response({'form':form})
            except:
                form.add_error('', 'Error Occured In Sending Mail, Try Again')
                messages.error(request, "Error Occured In Sending Mail, Try Again")
                return self.render_to_response({'form':form})
        else:
            return response

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('/')


# def login_request(request):
#     if request.method=='POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(email=email, password=password)
#             if user is not None :
#                 login(request,user)
#                 return redirect('/')
#             else:
#                 messages.error(request,"Invalid email or password")
#         else:
#                 messages.error(request,"Invalid email or password")
#     return render(request, '../templates/login.html',
#     context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

class LoginViewUser(LoginView):
    template_name = "login.html"

# class LogoutViewUser(LogoutView):
#     success_url = reverse_lazy('index')   

class HomePageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'home'
    template_name = "index.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')
# class Home1PageView(ListView):
#     paginate_by = 9
#     model = Appointment
#     context_object_name = 'home'
#     template_name = "index1.html"

#     def get_queryset(self):
#         return self.model.objects.all().order_by('-id')
