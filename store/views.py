from itertools import product
from django.shortcuts import render,get_object_or_404
from cart.models import Cart_item
from .models import Product
from category.models import Category
from cart.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def store(request, category_slug=None):

    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)


    
    context = {'products':paged_products,'products_count':products_count }
    return render(request,"store/store.html",context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = Cart_item.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        #Query to check the product if its aleady added to cart or not(reason for doing this if item is already in cart,then we shouldn't have the option to add it in cart again other than increment it from cart page)
        # return HttpResponse(in_cart)
        # exit()

    except Exception as e:
        raise e
    context = {'single_product': single_product,'in_cart':in_cart}
    return render(request,'store/product_detail.html',context)


