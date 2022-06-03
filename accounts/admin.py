from django.contrib import admin
from .models import User, Patient, Doctor
from .models import DoctorAdditional , PatientAdditional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class DoctorAdditionalInline(admin.TabularInline):
    model = DoctorAdditional

class PatientAdditionalInline(admin.TabularInline):
    model = PatientAdditional

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions','is_Doctor','is_Patient')}),   #'is_customer' , 'is_Doctor'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'name',  'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class DoctorAdmin(admin.ModelAdmin):
    inlines = (
        DoctorAdditionalInline,
    )
    # actions = ('merge', )
    # def merge(self, request, queryset):
    #     main = queryset[0]
    #     tail = queryset[1:]
    
    #     related = main._meta.get_all_related_objects()
    
    #     valnames = dict()
    #     for r in related:
    #         valnames.setdefault(r.model, []).append(r.field.name)
    
    #     for place in tail:
    #         for model, field_names in valnames.iteritems():
    #             for field_name in field_names:
    #                 model.objects.filter(**{field_name: place}).update(**{field_name: main})
    
    #         place.delete()
    
    #     self.message_user(request, "%s is merged with other places, now you can give it a canonical name." % main)
    
    
class PatientAdmin(admin.ModelAdmin):
    inlines = (
        PatientAdditionalInline,
    )



admin.site.register(CustomUser, CustomUserAdmin)






admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorAdditional)
admin.site.register(PatientAdditional)
