from django.shortcuts import render

# Create your views here.
from .models import Product


def product(request):
    products = Product.objects.all().filter(is_available=True)

    print(products)

    context = {'products':products}

    return render(request,'index.html',context)
