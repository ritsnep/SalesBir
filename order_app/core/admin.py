from venv import logger
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ValidationError
from .models import User, Company

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Company Info', {'fields': ('role', 'company')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            logger.error(f"Validation error while saving user: {e}")
            form.add_error(None, e)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
