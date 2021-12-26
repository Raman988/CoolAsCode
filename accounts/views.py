from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from django.views.generic import CreateView
from .form import PatientSignUpForm, DoctorSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
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

def register(request):
    return render(request, '../templates/register.html')

class Patient_register(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = '../templates/Patient_register.html'
    success_url = reverse_lazy('Patient_register')

    def post(self, request, *args, **kwargs):
        #form = RegistrationForm(request.POST)
        user_email = request.POST.get('email')
        try:
            existing_user = User.objects.get(email = user_email)
            if(existing_user.is_active == False):
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            user = User.objects.get(email = user_email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)     #www.wondershop.in:8000  127.0.0.1:8000 
            mail_subject = 'Activate your account.'
            message = render_to_string('../templates/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #print(message)
            to_email = user_email   
            #form = RegistrationForm(request.POST)   # here we are again calling all its validations
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
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
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
    model = User
    form_class = DoctorSignUpForm
    template_name = '../templates/Doctor_register.html'
    success_url = reverse_lazy('Doctor_register')

    def post(self, request, *args, **kwargs):
        #form = RegistrationForm(request.POST)
        user_email = request.POST.get('email')
        try:
            existing_user = User.objects.get(email = user_email)
            if(existing_user.is_active == False):
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            user = User.objects.get(email = user_email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)     #www.wondershop.in:8000  127.0.0.1:8000 
            mail_subject = 'Activate your account.'
            message = render_to_string('../templates/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #print(message)
            to_email = user_email   
            #form = RegistrationForm(request.POST)   # here we are again calling all its validations
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


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')
