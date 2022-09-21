from django.contrib import admin
from .models import Cart,Cart_item

# Register your models here.

class CartitemAdmin(admin.ModelAdmin):
    list_display = ['product','cart','quantity','is_active']


class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id','date_added']


admin.site.register(Cart,CartAdmin)
admin.site.register(Cart_item,CartitemAdmin)

