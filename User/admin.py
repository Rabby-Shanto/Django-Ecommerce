from django.contrib import admin

from .models import UserAcc

# Register your models here.

@admin.register(UserAcc)

class UseraccModel(admin.ModelAdmin):
    list_display = ['first_name','last_name','username','email','is_active','date_joined','last_login']


