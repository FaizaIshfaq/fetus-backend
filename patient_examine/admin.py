from django.contrib import admin

from .models import PatientFemurExamine, PatientHeadExamine


class PatientFemurExamineAdmin(admin.ModelAdmin):
    list_display = ('id', 'femur_length', 'femur_age')
    ordering = ['id']
    readonly_fields = ('femur_length', 'femur_age')


class PatientHeadExamineAdmin(admin.ModelAdmin):
    list_display = ('id', 'head_circumference', 'gestational_age')
    ordering = ['id']
    readonly_fields = ('head_circumference', 'gestational_age')


admin.site.register(PatientFemurExamine, PatientFemurExamineAdmin)
admin.site.register(PatientHeadExamine, PatientHeadExamineAdmin)
