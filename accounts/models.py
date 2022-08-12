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

   



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
  

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
   
class DoctorAdditional(models.Model):
    user = models.OneToOneField(Doctor, on_delete = models.CASCADE)
    location = models.CharField(max_length=20)
    your_expertise =  models.CharField(max_length=20)
   
