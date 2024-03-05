from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ['email', 'phone_number', 'is_active']
    list_display = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['id']
    readonly_fields = ('password',)


admin.site.register(User, UserAdmin)
