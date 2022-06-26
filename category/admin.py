from django.contrib import admin
from .models import Category

# Register your models here.

@admin.register(Category)

class catAdmin(admin.ModelAdmin):
    
    list_display = ['category_name','category_img','slug','description']
