# accounts/admin.py
from django.contrib import admin
from .models import CustomUser  # Импортируй свою кастомную модель

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)

admin.site.register(CustomUser, CustomUserAdmin)



