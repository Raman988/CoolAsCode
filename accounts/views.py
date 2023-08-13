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
def patient_register(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')

            try:
                existing_user = get_user_model().objects.get(email=user_email)
                if not existing_user.is_active:
                    existing_user.delete()
            except get_user_model().DoesNotExist:
                pass

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            age = form.cleaned_data.get('age')
            profile_photo = form.cleaned_data.get('profile_photo')

            patient_additional = PatientAdditional.objects.create(user=user, age=age, profile_photo=profile_photo)

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_email

            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[to_email],
                    fail_silently=False,
                )
                messages.success(request, "A link has been sent to your email id. Please check your inbox and spam folder.")
                return HttpResponseRedirect(reverse_lazy('accounts:Patient_register'))
            except:
                form.add_error(None, 'An error occurred while sending the email. Please try again.')
                messages.error(request, "An error occurred while sending the email. Please try again.")
    else:
        form = PatientSignUpForm()

    context = {'form': form}
    return render(request, 'Patient_register.html', context)

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
        return redirect(reverse_lazy('accounts:index'))
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')    
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
def doctor_register(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')

            try:
                existing_user = get_user_model().objects.get(email=user_email)
                if not existing_user.is_active:
                    existing_user.delete()
            except get_user_model().DoesNotExist:
                pass

            user = form.save(commit=False)
            user.is_active = False
            user.is_Doctor =True
            user.is_Patient= False
            user.save()

            location = form.cleaned_data.get('location')
            your_expertise = form.cleaned_data.get('your_expertise')

            DoctorAdditional.objects.create(user=user, location=location, your_expertise=your_expertise)

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_email

            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[to_email],
                    fail_silently=False,
                )
                messages.success(request, "A link has been sent to your email id. Please check your inbox and spam folder.")
                return HttpResponseRedirect(reverse_lazy('accounts:Doctor_register'))
            except:
                form.add_error(None, 'An error occurred while sending the email. Please try again.')
                messages.error(request, "An error occurred while sending the email. Please try again.")
    else:
        form = DoctorSignUpForm()

    context = {'form': form}
    return render(request, 'Doctor_register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')

class LoginViewUser(LoginView):
    template_name = "login.html"



class HomePageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'home'
    template_name = "index.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')
