from django.contrib import admin

from .models import Patient


class PatientAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'last_name', 'email', 'phone_number', 'is_active')
    list_display = ('id', 'first_name', 'last_name', 'blood_group', 'age', 'phone_number', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ['id']


admin.site.register(Patient, PatientAdmin)
