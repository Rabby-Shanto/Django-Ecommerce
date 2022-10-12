from itertools import product
from django.shortcuts import render,get_object_or_404
from cart.models import Cart_item
from rating.models import ReviewRating
from .models import Product
from category.models import Category
from cart.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from order.models import OrderedProduct
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Count

# Create your views here.
def store(request, category_slug=None):

    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category=categories,is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
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

    if request.user.is_authenticated:

        try:
            ordered_product = OrderedProduct.objects.filter(user=request.user,product_id=single_product.id).exists()

        except OrderedProduct.DoesNotExist:
            ordered_product = None

    else:
        ordered_product = None
    
    # get thee review from database

    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)


    #getting average rating of a product
    rating = ReviewRating.objects.filter(product=single_product,status=True).aggregate(average=Avg('rating'))
    avg = 0
    if rating['average'] is not None:
        avg = float(rating['average'])

    #counting reviews
    ratingCount = ReviewRating.objects.filter(product=single_product,status=True).aggregate(count=Count('id'))
    count = 0
    if ratingCount['count'] is not None:
        count = int(ratingCount['count'])



    context = {'single_product': single_product,'in_cart':in_cart,'ordered_product':ordered_product,'reviews':reviews,'avg': avg,'count':count}
    return render(request,'store/product_detail.html',context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword'] #storing the value of keyword e.g http://127.0.0.1:8000/store/search/?keyword=shirts(here keyword has the value of shirt)

        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))#for making complex queries,we use Q.here filter method doesn't support OR operation.
            products_count = products.count()

            context = {'products' : products , 'products_count' : products_count,'keyword': keyword}

    return render(request,'store/store.html',context)


