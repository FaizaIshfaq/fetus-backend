from django.contrib import admin

from .models import PatientExamine


class PatientExamineAdmin(admin.ModelAdmin):
    list_display = ('id', 'femur_number', 'femur_length', 'gestational_age')
    ordering = ['id']
    readonly_fields = ('femur_number', 'femur_length', 'gestational_age')


admin.site.register(PatientExamine, PatientExamineAdmin)
