from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Projekat.accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'institution', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Dodatna polja', {'fields': ('phone_number', 'institution', 'bio')}),
    )
# Register your models here.
