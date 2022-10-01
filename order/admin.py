from django.contrib import admin
from .models import Order,OrderedProduct,Payment

# Register your models here.

class OrderProductinline(admin.TabularInline):
    model = OrderedProduct
    readonly_fields = ['payment','user','product','quantity','product_price','is_ordered']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone','email','city','order_total','status','ip','is_ordered','created_at']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','first_name','last_name','phone','email']
    list_per_page = 20
    inlines = [OrderProductinline]

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedProduct)
admin.site.register(Payment)

