from django.contrib import admin

from .models import Doctor


class DoctorAdmin(admin.ModelAdmin):
    list_filter = ['name', 'specialization']
    list_display = ['id', 'name', 'specialization']
    search_fields = ['name', 'specialization']
    ordering = ['id']


admin.site.register(Doctor, DoctorAdmin)
