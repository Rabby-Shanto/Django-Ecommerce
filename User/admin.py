from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAcc

# Register your models here.

@admin.register(UserAcc)

class UseraccModel(UserAdmin):
    list_display = ['first_name','last_name','username','email','is_active','date_joined','last_login']
    filter_horizontal = ()
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('date_joined','last_login')
    list_filter = ()
    fieldsets = () #to make the password readonly

