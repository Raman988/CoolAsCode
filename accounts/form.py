from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, DoctorAdditional,PatientAdditional
from django import forms
from django.db import transaction
# from .models import User
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
    age = forms.CharField(required=True, max_length=5)
    gender = forms.CharField(required=True,label='Gender', widget=forms.RadioSelect(choices=GENDER_CHOICES))
    # gender = forms.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)

    class Meta:
        model = Patient
        fields = [
            'name',
            'email',
            'password1',
            'password2',
            'phone_number',
            'age',
            'gender',
        ]


# class PatientSignUpForm2(forms.ModelForm):
#     class Meta:
#         model = PatientAdditional
#         fields = [
#             'age',
#         ]    
    # @transaction.atomic
    # def save(self):
    #     Customuser = super().save(commit=False)
    #     # user.is_Patient = True
    #     Customuser.email = self.cleaned_data.get('email')
    #     Customuser.save()
    #     patient = Patient.objects.create(user=Customuser)
    #     # patient.phone_number=self.cleaned_data.get('phone_number')
    #     patient.age=self.cleaned_data.get('age')
    #     patient.gender=self.cleaned_data.get('gender')
    #     patient.save()
    #     return Customuser

class DoctorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True,max_length=50)
    your_expertise = forms.CharField(required=True,max_length=20)
    gender = forms.CharField(required=True,label='Gender', widget=forms.RadioSelect(choices=GENDER_CHOICES))

    class Meta:
        model = Doctor
        fields = [
            'name',
            'email',
            'password1',
            'password2',
            'phone_number',
            'location',
            'your_expertise',
            'gender',

        ]


    # @transaction.atomic
    # def save(self):
    #     Customuser = super().save(commit=False)
    #     # user.is_Doctor = True
    #     Customuser.is_staff = True
    #     Customuser.email = self.cleaned_data.get('email')
    #     Customuser.save()
    #     doctor = Doctor.objects.create(user=Customuser)
    #     doctor.phone_number=self.cleaned_data.get('phone_number')
    #     doctor.location=self.cleaned_data.get('location')
    #     doctor.gender=self.cleaned_data.get('gender')
    #     doctor.your_expertise=self.cleaned_data.get('your_expertise')
    #     doctor.save()
    #     return Customuser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)



class PatientProfileUpdateForm(forms.ModelForm):
    # age = forms.CharField(required=True, max_length=5)


    def __init__(self, *args, **kwargs):
        super(PatientProfileUpdateForm, self).__init__(*args, **kwargs)
        # user=self.user
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )
        # self.fields['last_name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Last Name',
        #     }
        # )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        ) 
        self.fields['gender'].widget.attrs.update(
            {
                'placeholder': 'gender',
            }
        )
        # self.request.showAdditional.fields['age'].widget.attrs.update(
        # self.fields['age'].widget.attrs.update(
        #     {
        #         'placeholder': 'age',
        #     }
        # )

    class Meta:
        model = Patient
        # , Patient.showAdditional
        fields = [
            "name",
        #  "last_name",
          "email",
           "phone_number",
        #    "age",

           "gender",

           ]

class PatientProfileUpdateForm2(forms.ModelForm):
    # age = forms.CharField(required=True, max_length=5)
    
    def __init__(self, *args, **kwargs):
        super(PatientProfileUpdateForm2, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Full Name',
        #     }
        # )
        # self.fields['last_name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Last Name',
        #     }
        # )
        # self.fields['email'].widget.attrs.update(
        #     {
        #         'placeholder': 'Email',
        #     }
        # )
        # self.fields['phone_number'].widget.attrs.update(
        #     {
        #         'placeholder': 'Phone Number',
        #     }
        # ) 
        # self.fields['gender'].widget.attrs.update(
        #     {
        #         'placeholder': 'gender',
        #     }
        # )
        # self.request.showAdditional.fields['age'].widget.attrs.update(
        self.fields['age'].widget.attrs.update(
            {
                'placeholder': 'age',
            }
        )

    class Meta:
        model = PatientAdditional
        # , Patient.showAdditional
        fields = [
            # "name",
        #  "last_name",
        #   "email",
        #    "phone_number",
           "age",

        #    "gender",

           ]


class DoctorProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )
        # self.fields['last_name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Last Name',
        #     }
        # )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        ) 
        self.fields['gender'].widget.attrs.update(
            {
                'placeholder': 'gender',
            }
        )
        # self.fields['your_expertise'].widget.attrs.update(
        #     {
        #         'placeholder': 'your_expertise',
        #     }
        # )
        # self.fields['location'].widget.attrs.update(
        #            {
        #                'placeholder': 'location',
        #            }
            #    )
       
    class Meta:
        model = Doctor
# ,Doctor.showAdditional
        fields = ["name", 
        # "last_name",
         "email",
        "gender",
        "phone_number",
        # "your_expertise",
        # "location",
         ]
         
class DoctorProfileUpdateForm2(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorProfileUpdateForm2, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Full Name',
        #     }
        # )
        # self.fields['last_name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Last Name',
        #     }
        # )
        # self.fields['email'].widget.attrs.update(
        #     {
        #         'placeholder': 'Email',
        #     }
        # )
        # self.fields['phone_number'].widget.attrs.update(
        #     {
        #         'placeholder': 'Phone Number',
        #     }
        # ) 
        # self.fields['gender'].widget.attrs.update(
        #     {
        #         'placeholder': 'gender',
        #     }
        # )
        self.fields['your_expertise'].widget.attrs.update(
            {
                'placeholder': 'your_expertise',
            }
        )
        self.fields['location'].widget.attrs.update(
                   {
                       'placeholder': 'location',
                   }
               )
       
    class Meta:
        model = DoctorAdditional
# ,Doctor.showAdditional
        fields = [
            # "name", 
        # "last_name",
        #  "email",
        # "gender",
        # "phone_number",
        "your_expertise",
        "location",
         ]