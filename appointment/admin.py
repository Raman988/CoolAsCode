from django.contrib import admin
from .models import Appointment, Order, PatientAppointmentTrack,TakeAppointment

class AppointmentInline(admin.TabularInline):
    model = Appointment

class TakeAppointmentInline(admin.TabularInline):
    model = TakeAppointment
class OrderInline(admin.TabularInline):
    model = Order
class TrackInline(admin.TabularInline):
    model = PatientAppointmentTrack


admin.site.register(Appointment)
admin.site.register(TakeAppointment)
admin.site.register(Order)
admin.site.register(PatientAppointmentTrack)
