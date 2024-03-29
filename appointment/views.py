from datetime import date
from django.shortcuts import render



from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect,HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from accounts.models import Doctor, User,Patient
from .decorators import user_is_patient, user_is_doctor
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView,View
from django.views.generic.edit import DeleteView, UpdateView
from accounts.form import DoctorProfileUpdateForm2, PatientProfileUpdateForm, DoctorProfileUpdateForm, PatientProfileUpdateForm2
from .forms import CreateAppointmentForm, TakeAppointmentForm
from .models import Appointment, PatientAppointmentTrack, TakeAppointment, Order
from accounts.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from docmed import settings




        


@login_required
def editprofile(request, id):
    try:
        obj = get_object_or_404(Patient, id=id)
        obj1 = PatientAdditional.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return HttpResponse('Patient not found.')
    except PatientAdditional.DoesNotExist:
        obj1 = PatientAdditional(user=request.user)

    if request.method == 'POST':
        form = PatientProfileUpdateForm(request.POST, instance=obj)
        form1 = PatientProfileUpdateForm2(request.POST,request.FILES or None, instance=obj1)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return HttpResponseRedirect("/" )
    else:
        form = PatientProfileUpdateForm(instance=obj)
        form1 = PatientProfileUpdateForm2(instance=obj1)

    context = {'form': form, 'form1': form1}
    return render(request, "accounts/patient/edit-profile-extra.html", context)


def editprofiledoctor(request,id):
   
    obj1=DoctorAdditional.objects.get(user=request.user)
    obj = get_object_or_404(Doctor, id=id)
 
    # pass the object as instance in form
    form = DoctorProfileUpdateForm(request.POST or None, instance = obj)
    form1 = DoctorProfileUpdateForm2 (request.POST or None, instance = obj1)
    try:
        obj2=Appointment.objects.get(user=request.user)
        form2 = CreateAppointmentForm (request.POST or None,request.FILES or None, instance = obj2)
    except:
        obj2=Appointment.objects.create(user=request.user)
        form2 = CreateAppointmentForm (request.POST or None,request.FILES or None, instance=obj2)

    # 
    if form.is_valid() and form1.is_valid() and form2.is_valid():
        form.save()
        form1.save()
        form2.save()

        return HttpResponseRedirect("/")
 
    # add form dictionary to context
    context={'form':form, 'form1':form1,'form2':form2}
    # context1["form1"] = form1
 
    return render(request, "accounts/doctor/edit-profile.html", context)
@login_required
def display_cart(request,id):
    try:
        qs = TakeAppointment.objects.get(id=id)
        appointment = get_object_or_404(Appointment, id=qs.appointment.id)
        return render(request, "payment/detail.html", {'cart': [appointment], 'id':id})
    except TakeAppointment.DoesNotExist:
        raise Http404("Appointment has already been taken.")

def doctordetails(request,id):
    # context={}
        
   
        if request.method == 'POST':
            appointment = Appointment.objects.get(id=id)
            message = request.POST.get('message')
            date = request.POST.get('date')
            time = request.POST.get('time')
            # 
            t_app = TakeAppointment.objects.create(appointment=appointment, user=request.user,message=message, date=date,time=time) 
            t_app.save()
            # return  redirect(reverse_lazy("appointment:detail"))
            return redirect('appointment:detail', t_app.id)
            # 
        return render(request, 'appointment/take_appointment_detail.html')
    
        #


"""
   For Doctor Profile
"""


# 






# 
def patient_list(request):
    patients = TakeAppointment.objects.filter(appointment__user_id=request.user.id).order_by('-id')
    
    context = {
        'patients': patients,
    }

    return render(request, 'appointment/patient_list.html', context)

def doctor_list(request):
    doctors = TakeAppointment.objects.filter(user__id=request.user.id).order_by('-id')
    
    context = {
        'doctors': doctors,
    }

    return render(request, 'appointment/doctor_list.html', context)




def delete_patient(request, pk):
    appointment = get_object_or_404(TakeAppointment, pk=pk)
    appointment.delete()
    return redirect('appointment:patient-list')

def delete_doctor(request, pk):
    appointment = get_object_or_404(TakeAppointment, pk=pk)
    appointment.delete()
    return redirect('appointment:doctor-list')







#


from django.views.generic import TemplateView

def service_view(request):
    template_name = 'appointment/service.html'
    return render(request, template_name)


from django.views.generic import ListView
from .models import DoctorAdditional

def search_view(request):
    paginate_by = 6
    model = DoctorAdditional
    template_name = 'appointment/search.html'
    context_object_name = 'appointment'

    if request.method == 'GET':
        your_expertise = request.GET.get('your_expertise')
        location = request.GET.get('location')
        queryset = model.objects.filter(
            your_expertise__contains=your_expertise,
            location__contains=location
        )
        context = {
            'appointment': queryset
        }
        return render(request, template_name, context)

# 



import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

from .models import Order
from django.contrib.sites.shortcuts import get_current_site


@login_required
def payment(request, id):
    if request.method == "POST":
        
        cart = TakeAppointment.objects.get(id = id)
        print(cart.id)
    
       
        order = Order.objects.create(take=cart, total_amount = 0)
        final_price= cart.appointment.price
        print(final_price)
        print(order)
       
        
        order.total_amount = final_price
        order.save()

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
        print(callback_url)
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=final_price*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        return render(request, 'payment/paymentsummaryrazorpay.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':final_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
    else:
        return HttpResponse("505 Not Found") 


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import EmailMessage



def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

from django.core.mail import EmailMultiAlternatives
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        # try:
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id','')
        signature = request.POST.get('razorpay_signature','')
        params_dict = { 
        'razorpay_order_id': order_id, 
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
        }
        try:
            order_db = Order.objects.get(razorpay_order_id=order_id)
        except:
            return HttpResponse("505 Not Found")
        order_db.razorpay_payment_id = payment_id
        order_db.razorpay_signature = signature
        order_db.save()
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result==None:
            amount = order_db.total_amount * 100   #we have to pass in paisa
            # try:
            razorpay_client.payment.capture(payment_id, amount)
            order_db.payment_status = 1
            order_db.save()

            template = get_template('payment/invoice.html')
            data = {
                'order_id': order_db.order_id,
                'transaction_id': order_db.razorpay_payment_id,
                'user_email': order_db.take.user.email,
                'date': str(order_db.datetime_of_payment),
                'name': order_db.take.user.name,
                'order': order_db,
                'amount': order_db.total_amount,
            }
            html  = template.render(data)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
            pdf = result.getvalue()
            filename = 'Invoice_' + data['order_id'] + '.pdf'

            mail_subject = 'Recent Order Details'
            message = render_to_string('payment/emailinvoice.html', {
                'user': order_db.take.user,
                'order': order_db
            })
            context_dict = {
                'user': order_db.take.user,
                'order': order_db
            }
            # template = get_template('payment/emailinvoice.html')
            # message  = template.render(context_dict)
            # to_email = order_db.user.email
            # email = EmailMessage(
            #     mail_subject,
            #     message, 
            #     settings.EMAIL_HOST_USER,
            #     [to_email]
            # )

            # # for including css(only inline css works) in mail and remove autoescape off
            # email = EmailMultiAlternatives(
            #     mail_subject,
            #     "hello",       # necessary to pass some message here
            #     settings.EMAIL_HOST_USER,
            #     [to_email]
            # )
            # email.attach_alternative(message, "text/html")
            # email.attach(filename, pdf, 'application/pdf')
            # email.send(fail_silently=False)

            return render(request, 'payment/paymentsuccess.html',{'id':order_db.id})
            # except:
            #     order_db.payment_status = 2
            #     order_db.save()
            #     return render(request, 'payment/paymentfailed.html')
        else:
            order_db.payment_status = 2
            order_db.save()
            return render(request, 'payment/paymentfailed.html')
        # except:
        #     return HttpResponse("505 not found")


class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            order_db = Order.objects.get(id = pk , payment_status = 1)     #you can filter using order_id as well
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.order_id,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.take.user.email,
            'date': str(order_db.datetime_of_payment),
            'name': order_db.take.user.name,
            'order': order_db,
            'amount': order_db.total_amount,
        }
        pdf = render_to_pdf('payment/invoice.html', data)

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



def view_doctor_detail(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    doctor = appointment.user
    
    context = {
        'doctor': doctor
    }
    
    return render(request, 'accounts/doctor/detail.html', context)