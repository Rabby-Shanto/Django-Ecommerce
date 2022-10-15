from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAcc,userProfile
from django.utils.html import format_html

# Register your models here.

@admin.register(UserAcc)


class UseraccModel(UserAdmin):
    list_display = ['first_name','last_name','username','email','is_active','date_joined','last_login']
    filter_horizontal = ()
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('date_joined','last_login')
    list_filter = ()
    fieldsets = () #to make the password readonly

@admin.register(userProfile)


class UserprofileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style = "border-radius : 50%" >'.format(object.profile_picture.url))
    thumbnail.short_description = "Profile Picture"
    list_display = ['thumbnail','user','city','state','country']



