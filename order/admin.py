from django.contrib import admin
from .models import Order,OrderedProduct,Payment

# Register your models here.


admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(Payment)

