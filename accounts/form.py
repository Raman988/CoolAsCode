from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User
from .models import Doctor,Patient
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
# DEPARTMENT_CHOICES= (
#     ('Dentistry', "Dentistry"),
#     ('Cardiology', "Cardiology"),
#     ('ENT Specialists', "ENT Specialists"),
#     ('Astrology', 'Astrology'),
#     ('Neuroanatomy', 'Neuroanatomy'),
#     ('Blood Screening', 'Blood Screening'),
#     ('Eye Care', 'Eye Care'),
#     ('Physical Therapy', 'Physical Therapy'),
# )


class PatientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    age = forms.CharField(required=True)
    gender = forms.CharField(required=True,label='Gender', widget=forms.RadioSelect(choices=GENDER_CHOICES))
    # gender = forms.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Patient = True
        user.email = self.cleaned_data.get('email')
        user.save()
        patient = Patient.objects.create(user=user)
        patient.phone_number=self.cleaned_data.get('phone_number')
        patient.age=self.cleaned_data.get('age')
        patient.gender=self.cleaned_data.get('gender')
        patient.save()
        return user

class DoctorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)
    your_expertise = forms.CharField(required=True)
    gender = forms.CharField(required=True,label='Gender', widget=forms.RadioSelect(choices=GENDER_CHOICES))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Doctor = True
        user.is_staff = True
        user.email = self.cleaned_data.get('email')
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.phone_number=self.cleaned_data.get('phone_number')
        doctor.location=self.cleaned_data.get('location')
        doctor.gender=self.cleaned_data.get('gender')
        doctor.your_expertise=self.cleaned_data.get('your_expertise')
        doctor.save()
        return user
