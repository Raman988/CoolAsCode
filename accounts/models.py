from re import T
from django.db import models



from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
# Create your models here.
from multiselectfield import MultiSelectField


from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
# from appointment.models import Appointment

from django.contrib.auth.models import PermissionsMixin

from django.db.models import Q
# from datetime import timedelta



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


# class User(AbstractUser):
#     is_Patient = models.BooleanField(default=False)
#     is_Doctor = models.BooleanField(default=False)

# class Patient(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
#     phone_number = models.CharField(max_length=20)
#     age = models.CharField(max_length=20)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)

# class Doctor(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
#     phone_number = models.CharField(max_length=20)
#     location = models.CharField(max_length=20)
#     your_expertise =  models.CharField(max_length=20)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    # if you require phone number field in your project
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone_number = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True)  # you can set it unique = True
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)
    
    is_Patient = models.BooleanField(default=True)
    is_Doctor = models.BooleanField(default = False)

    # type = (
    #     (1, 'Doctor'),
    #     (2, 'Patient')
    # )
    # user_type = models.IntegerField(choices = type, default=1)

    #usertype = models.ManyToManyField(UserType)

    # class Types(models.TextChoices):
    #     DOCTOR = "Doctor", "DOCTOR"
    #     PATIENT = "Patient", "PATIENT"
    
    # Types = (
    #     (1, 'Doctor'),
    #     (2, 'Patient')
    # )
    # type = models.IntegerField(choices=Types, default=2)

    # default_type = Types.PATIENT

    #type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)
    # type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
    #place here
        # if not the code below then taking default value in User model not in proxy models
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         #self.type = self.default_type
    #         self.type.append(self.default_type)
    #     return super().save(*args, **kwargs)


# Model Managers for proxy models
class DoctorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.Doctor)
        return super().get_queryset(*args, **kwargs).filter(is_Doctor=True)

class PatientManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.Patient)
        return super().get_queryset(*args, **kwargs).filter(is_Patient=True)


# Proxy Models. They do not create a seperate table
class Doctor(CustomUser):
    # default_type = CustomUser.Types.DOCTOR
    is_Doctor = True
    objects = DoctorManager()
    class Meta:
        proxy = True
    
    # def sell(self):
    #     print("I can sell")

    @property
    def showAdditional(self):
        return self.doctoradditional

    @property
    def showAppointment(self):
        return self.appointment
        
    def __str__(self):
        return self.name  
    
class Patient(CustomUser):
    # default_type = CustomUser.Types.PATIENT
    is_Patient= True
    objects = PatientManager()
    class Meta:
        proxy = True 

    # def buy(self):
    #     print("I can buy")

    @property
    def showAdditional(self):
        return self.patientadditional
    @property
    def age(self):
        return self.patientadditional.age

    @age.setter
    def age(self, age):
        self.patientadditional.age = age  
            
    def __str__(self):
        return self.name 

class PatientAdditional(models.Model):
    user = models.OneToOneField(Patient, on_delete = models.CASCADE)
    age = models.CharField(max_length=20)
    # role = models.CharField(max_length=20, default="patient")
    
    # patient_id = models.AutoField(primary_key=True)
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)

class DoctorAdditional(models.Model):
    user = models.OneToOneField(Doctor, on_delete = models.CASCADE)
    location = models.CharField(max_length=20)
    your_expertise =  models.CharField(max_length=20)
    # role = models.CharField(max_length=20, default="doctor")
    
    # doctor_id = models.AutoField(primary_key=True)

    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)
