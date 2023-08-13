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
    profile_photo = forms.ImageField(required=False)
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
            'profile_photo',
        ]




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


    

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)



class PatientProfileUpdateForm(forms.ModelForm):
   


    def __init__(self, *args, **kwargs):
        super(PatientProfileUpdateForm, self).__init__(*args, **kwargs)
        # user=self.user
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )
      
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
    profile_photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(PatientProfileUpdateForm2, self).__init__(*args, **kwargs)
        
        self.fields['age'].widget.attrs.update({
            'placeholder': 'Age',
        })
        
        self.fields['profile_photo'].widget.attrs.update({
            'class': 'form-control-file',
        })

    class Meta:
        model = PatientAdditional
        fields = ['age', 'profile_photo',]


class DoctorProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )
       
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
