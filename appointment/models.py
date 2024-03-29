from django.db import models
from django.urls import reverse
from django.utils import timezone
from accounts.models import CustomUser ,Doctor, DoctorAdditional,Patient 

from datetime import date, datetime

import appointment

# Create your models here.

# class Order(models.Model):
#     status_choices = (
#         (1, 'Not Packed'),
#         (2, 'Ready For Shipment'),
#         (3, 'Shipped'),
#         (4, 'Delivered')
#     )
#     payment_status_choices = (
#         (1, 'SUCCESS'),
#         (2, 'FAILURE' ),
#         (3, 'PENDING'),
#     )
    
#     user = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     status = models.IntegerField(choices = status_choices, default=1)
    
    

#     total_amount = models.FloatField()
#     payment_status = models.IntegerField(choices = payment_status_choices, default=3)
#     order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
#     datetime_of_payment = models.DateTimeField(default=timezone.now)
#     # related to razorpay
#     razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
#     razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
#     razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    

#     def save(self, *args, **kwargs):
#         if self.order_id is None and self.datetime_of_payment and self.id:
#             self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
#         return super().save(*args, **kwargs)

#     def __str__(self):
#         return self.user.email + " " + str(self.id) 
class Appointment(models.Model):
    user = models.OneToOneField(Doctor,on_delete=models.CASCADE)
    #
    image = models.ImageField(null=True, blank=True)
    #
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    qualification_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    price= models.FloatField(max_length=10, default='500')
    # 
    created_at = models.DateTimeField(default=timezone.now)
    # 
    
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/about.jpg"


    def __str__(self):
        return self.user.name
 
class TakeAppointment(models.Model):
    # 
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateField(auto_now_add=False,default=date.today)
    time = models.TimeField(auto_now_add=False,default=timezone.now)
    # time = models.TimeField()
    
    def __str__(self):
        return self.user.name

class Order(models.Model):
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    
    take = models.ForeignKey(TakeAppointment, on_delete=models.CASCADE )
    status = models.IntegerField(choices = status_choices, default=1)
    
    

    total_amount = models.FloatField()
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.take.user.email + " " + str(self.id)  




class PatientAppointmentTrack(models.Model):
    # 
    user = models.OneToOneField(Patient,on_delete=models.CASCADE)
    # 
    price= models.FloatField(max_length=10, default='500')
    # 
    created_at = models.DateTimeField(default=timezone.now)
    appointment = models.ForeignKey(Order, on_delete = models.CASCADE)

    
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/about.jpg"


    def __str__(self):
        return self.user.name




