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
from docmed import settings

"""
For Patient Profile
    
"""
# Create your views here.
# class ProductDetail(DetailView):
#     model = Product
#     template_name = "firstapp/productdetail.html"
#     context_object_name = "product"

class EditPatientProfileView(UpdateView):
    model=Patient
    form_class = PatientProfileUpdateForm
    template_name = 'accounts/patient/edit-profile.html'
    success_url = reverse_lazy('accounts:index')
    # success_message = "Redirect successfully created!"
    context_object_name = 'patient'



    # def post(self, request,pk,*args, **kwargs):
    #     # form = PatientSignUpForm(request.POST)
    #     # user_email = request.POST.get('email')
        
    #     # try:
    #     #     existing_user = CustomUser.objects.get(email = user_email)
    #     #     if(existing_user.is_active == False):
    #     #         existing_user.delete()
    #     # except:
    #     #     pass
    #     response = super().post(request, *args, **kwargs)
    #     if response.status_code == 302:
    #         age = request.POST.get('age')
    #         # gender = request.POST.get('gender')
    #         user = Patient.objects.get(id=pk)
    #         s_add = PatientAdditional.objects.create(user = user, age = age)
    #         # user.is_active = False
    #         s_add.save()
    # model = Patient
    # form_class = PatientProfileUpdateForm #,PatientProfileUpdateForm2
    # # context_object_name = 'patient'
    # template_name = 'accounts/patient/edit-profile.html'
    # # success_url = reverse_lazy('appointment:patient-list')
    # success_url = reverse_lazy('accounts:patient-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_patient)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    # def get_context_data(self, **kwargs):
    #     kwargs.setdefault('view', self)
    #     if self.extra_context is not None:
    #         kwargs.update(self.extra_context)
    #     return kwargs    

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        obj.save()
        if obj is None:
            raise Http404("Patient doesn't exists")
        return obj
        
    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     if response.status_code == 302:

    #        # if int(request.POST.get("quantity")) == 0:
    #        #     productincart = self.get_object()
    #        #     productincart.delete()
    #         return response
    #     else:

    #         messages.error(request, "error in quantity")
    #         return redirect(reverse_lazy("accounts:patient-profile-update"))  

    
# class EditPatientProfileView1(UpdateView):
#     model=PatientAdditional
#     form_class = PatientProfileUpdateForm2
#     template_name = 'accounts/patient/edit-profile-extra.html'
#     success_url = reverse_lazy('accounts:index')
#     # success_message = "Redirect successfully created!"
#     context_object_name = 'patient'

#     @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
#     @method_decorator(user_is_patient)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(self.request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         try:
#             self.object = self.get_object()
#         except Http404:
#             raise Http404("User doesn't exists")
#         # context = self.get_context_data(object=self.object)
#         return self.render_to_response(self.get_context_data())


#     def get_object(self, queryset=None):
#         obj = self.request.user
#         print(obj)
#         obj.save()
#         if obj is None:
#             raise Http404("Patient doesn't exists")
#         return obj
        
def editprofile(request,id):
    context ={}
 
    # fetch the object related to passed id
    obj1=PatientAdditional.objects.get(user=request.user)
    obj = get_object_or_404(Patient, id=id)
 
    # pass the object as instance in form
    form1 = PatientProfileUpdateForm2(request.POST or None, instance = obj1)
    form = PatientProfileUpdateForm(request.POST or None, instance = obj)
    # user =CustomUser.objects.get(id=id)
    # age = request.POST.get('age')
    # s_add=PatientAdditional.objects.get(id=id,age=age)
    # s_add.save()
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid() and form1.is_valid():
        form.save()
        form1.save()
        return HttpResponseRedirect("/"+id)
 
    # add form dictionary to context
    context={'form':form, 'form1':form1}
    # context1["form1"] = form1
    return render(request, "accounts/patient/edit-profile-extra.html", context)

def editprofiledoctor(request,id):
    # context ={}
    # context1 ={}
 
    # fetch the object related to passed id
    obj1=DoctorAdditional.objects.get(user=request.user)
    obj = get_object_or_404(Doctor, id=id)
 
    # pass the object as instance in form
    form = DoctorProfileUpdateForm(request.POST or None, instance = obj)
    form1 = DoctorProfileUpdateForm2 (request.POST or None, instance = obj1)
    try:
        obj2=Appointment.objects.get(user=request.user)
        form2 = CreateAppointmentForm (request.POST or None,request.FILES or None, instance = obj2)
        # img_object = form2.instance  
    except:
        obj2=Appointment.objects.create(user=request.user)
        form2 = CreateAppointmentForm (request.POST or None,request.FILES or None, instance=obj2)
        # img_object = form2.instance  

    # user =CustomUser.objects.get(id=id)
    # age = request.POST.get('age')
    # s_add=PatientAdditional.objects.get(id=id,age=age)
    # s_add.save()
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid() and form1.is_valid() and form2.is_valid():
        form.save()
        form1.save()
        form2.save()

        return HttpResponseRedirect("/")
 
    # add form dictionary to context
    context={'form':form, 'form1':form1,'form2':form2}
    # context1["form1"] = form1
 
    return render(request, "accounts/doctor/edit-profile.html", context)

class DisplayCart(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "payment/detail.html"
    context_object_name = "cart"

    def get_queryset(self):
        try:
           qs = TakeAppointment.objects.get(user = self.request.user)
           queryset=Appointment.objects.filter(id= qs.appointment.id)
           return queryset
        except:
           raise Http404("appointment has already taken ")

def doctordetails(request,id):
    # context={}
        
   
        if request.method == 'POST':
            # form = TakeAppointmentDetailForm(request.POST)
            appointment = Appointment.objects.get(id=id)
            # full_name = request.POST.get('full_name')
            message = request.POST.get('message')
            date = request.POST.get('date')
            time = request.POST.get('time')
            # phone_number = request.POST.get('phone_number')
            # user = User.objects.get(user =request.user)
            t_app = TakeAppointment.objects.create(appointment=appointment, user=request.user,message=message, date=date,time=time) 
            t_app.save()
            return  redirect(reverse_lazy("appointment:detail"))
            # context={'apt': appointment}
        return render(request, 'appointment/take_appointment_detail.html')
    
        # form = request.get_form()
        # if form.is_valid():      #clean_data
        #     if len(form.cleaned_data.get('message'))>20:
        #         form.add_error('message', 'Query length is not right')
        #         return render(request, 'appointment/take_appointment_detail.html', {'form':form})
        #     form.save()
        # return HttpResponse("Thank YOu")

class TakeAppointmentView(CreateView):
    template_name = 'appointment/take_appointment.html'
    form_class = TakeAppointmentForm
    extra_context = {
        'title': 'Take Appointment'
    }
    success_url = reverse_lazy('appointment:detail')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.is_Doctor:
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TakeAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


"""
   For Doctor Profile
"""


# class EditDoctorProfileView(UpdateView):
#     model = Doctor
#     form_class = DoctorProfileUpdateForm
#     context_object_name = 'doctor'
#     template_name = 'accounts/doctor/edit-profile.html'
#     success_url = reverse_lazy('accounts:doctor-profile-update')

#     @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
#     @method_decorator(user_is_doctor)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(self.request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         try:
#             self.object = self.get_object()
#         except Http404:
#             raise Http404("User doesn't exists")
#         # context = self.get_context_data(object=self.object)
#         return self.render_to_response(self.get_context_data())

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         print(obj)
#         if obj is None:
#             raise Http404("Patient doesn't exists")
#         return obj


class AppointmentCreateView(CreateView):
    template_name = 'appointment/appointment_create.html'
    form_class = CreateAppointmentForm
    extra_context = {
        'title': 'Post New Appointment'
    }
    success_url = reverse_lazy('appointment:doctor-appointment')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_doctor)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        # if self.request.user.is_authenticated and self.request.user.Types != 'DOCTOR':
        #     return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AppointmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_doctor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


class PatientListView(ListView):
    model = TakeAppointment
    context_object_name = 'patients'
    template_name = "appointment/patient_list.html"

    def get_queryset(self):
        return self.model.objects.filter(appointment__user_id=self.request.user.id).order_by('-id') 


class PatientDeleteView(DeleteView):
    model = TakeAppointment
    success_url = reverse_lazy('appointment:patient-list')


class AppointmentDeleteView(DeleteView):
    """
       For Delete any Appointment created by Doctor
    """
    model = Appointment
    success_url = reverse_lazy('appointment:doctor-appointment')


"""
   For both Profile
   
"""


# class HomePageView(ListView):
#     paginate_by = 9
#     model = Appointment
#     context_object_name = 'home'
#     template_name = "home.html"

#     def get_queryset(self):
#         return self.model.objects.all().order_by('-id')


class ServiceView(TemplateView):
    template_name = 'appointment/service.html'


class SearchView(ListView):
    paginate_by = 6
    model = DoctorAdditional
    template_name = 'appointment/search.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return self.model.objects.filter(
            your_expertise__contains=self.request.GET['your_expertise'],
                                         location__contains=self.request.GET['location'],
                                        #  name__contains=self.request.GET['name']
                                         )

# class UpdatePatient(LoginRequiredMixin, UpdateView):
#     model = Patient
#     form_class = PatientProfileUpdateForm
#     success_url = reverse_lazy("accounts:patient-profile-update")

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 302:
#             # if int(request.POST.get("quantity")) == 0:
#             #     productincart = self.get_object()
#             #     productincart.delete()
#             return response
#         else:
#             messages.error(request, "error in quantity")
#             return redirect(reverse_lazy("accounts:patient-profile-update"))   

# def search(request):
#     info={}
#     # qs=Appointment.objects.all()
#     # d_add = DoctorAdditional.objects.all()
#     # ms= qs.user.all()
#     qs = Appointment.objects.all()

#     name_contains_query=request.GET.get('name')
#     specialist_contains_query=request.GET.get('your_expertise')
#     city_contains_query=request.GET.get('location')
#     if name_contains_query!='' and name_contains_query is not None:
#         ms=Doctor.objects.get(name__icontains=name_contains_query)
#         qs=Appointment.objects.get(user=ms.id)
#         info={'appointment':qs}

#     if specialist_contains_query!='' and specialist_contains_query is not None:
#         d_add=DoctorAdditional.objects.get(user=ms.id ,your_expertise__icontains=specialist_contains_query)
#         qs=Appointment.objects.filter(user=d_add.user.id)
#         info={'appointment':qs}
        
        
      
#     if city_contains_query!='' and city_contains_query is not None:
#         d_add1=DoctorAdditional.objects.get(id=d_add.id,location__icontains=city_contains_query)
#         # qs=Appointment.objects.all()

#         qs=Appointment.objects.filter(user=d_add1.user.id)
    
#         info={'appointment':qs}

    
#     return render(request,"appointment/search.html",info)



import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

from .models import Order
from django.contrib.sites.shortcuts import get_current_site


@login_required
def payment(request):
    if request.method == "POST":
        
        cart = TakeAppointment.objects.get(user = request.user)
        products_in_cart =Appointment.objects.filter(id= cart.appointment.id)

        # products_in_cart = Appointment.objects.filter(id = id)
        # products_in_cart = Appointment.objects.filter(id = id)
        final_price = 0
    
        # try:
        #     if(len(products_in_cart)>0):
                # order = Order.objects.create(user = request.user, total_amount = 0)
                # order.save()
        order = Order.objects.create(user = request.user, total_amount = 0)
        for product in products_in_cart:
            final_price = product.price
            product_in_order = PatientAppointmentTrack.objects.create(appointment = order,  user=request.user, price = product.price)
        #         else:
        #            return HttpResponse("No product in cart")
        # except:
        #     return HttpResponse("No product in cart")
        
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


# for generating pdf invoice
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

            ## For generating Invoice PDF
            template = get_template('payment/invoice.html')
            data = {
                'order_id': order_db.order_id,
                'transaction_id': order_db.razorpay_payment_id,
                'user_email': order_db.user.email,
                'date': str(order_db.datetime_of_payment),
                'name': order_db.user.name,
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
                'user': order_db.user,
                'order': order_db
            })
            context_dict = {
                'user': order_db.user,
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
            order_db = Order.objects.get(id = pk, user = request.user, payment_status = 1)     #you can filter using order_id as well
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.order_id,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.datetime_of_payment),
            'name': order_db.user.name,
            'order': order_db,
            'amount': order_db.total_amount,
        }
        pdf = render_to_pdf('payment/invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



