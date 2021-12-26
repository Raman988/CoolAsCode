from django.db import models
from django.contrib.auth.models import AbstractUser
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
class User(AbstractUser):
    is_Patient = models.BooleanField(default=False)
    is_Doctor = models.BooleanField(default=False)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    your_expertise =  models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)


