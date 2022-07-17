from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart,Cart_item

from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.




def cart(request,total=0,quantity=0,tax=0,grand_total=0,cart_items=None):

    try:
        if request.user.is_authenticated:
            cart_items = Cart_item.objects.filter(user=request.user,is_active=True)

        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = Cart_item.objects.filter(cart=cart,is_active=True)
            
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (3 * total)/100
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'total' : total,
        'quantity' : quantity,
        'grand_total' : grand_total,
        'tax': tax,
    }

    return render(request,'store/cart.html',context)



def _cart_id(request):

    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request,product_id):
    current_user = request.user
    #........Getting Product................
    product = Product.objects.get(id=product_id) #fetch the product base on id
    # Getting Product Variation
    # if user is authenticated

    if current_user.is_authenticated:

        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                # print(key,value) #Here getting the product variation as key and value. For exaple: key = color and value=red or key = size value = large
                try:
                    variation = Variation.objects.get(product = product,variation_class__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        #..................Getting Cart item ...................
        is_cartitem_exists = Cart_item.objects.filter(product=product,user=current_user)

        if is_cartitem_exists:

            cart_item = Cart_item.objects.filter(product=product, user = current_user)
            #Adding Cart Item
            ex_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_variation_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_variation_list:
                index = ex_variation_list.index(product_variation)
                item_id = id[index]
                #increasing cart_item quantity
                item = Cart_item.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = Cart_item.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()

        else:
            cart_item = Cart_item.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )

            cart_item.variations.clear()
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect('cart')

    #if user is not authenticated
    
    else:

        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                # print(key,value) #Here getting the product variation as key and value. For exaple: key = color and value=red or key = size value = large
                try:
                    variation = Variation.objects.get(product = product,variation_class__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        #....................Getting Cart...................
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            #to get the cart using cart id present in session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )

        cart.save()

        #..................Getting Cart item ...................
        is_cartitem_exists = Cart_item.objects.filter(product=product,cart=cart)

        if is_cartitem_exists:

            cart_item = Cart_item.objects.filter(product=product, cart = cart)
            #Adding Cart Item
            ex_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_variation_list.append(list(existing_variation))
                id.append(item.id)

            # print(ex_variation_list)

            if product_variation in ex_variation_list:
                index = ex_variation_list.index(product_variation)
                item_id = id[index]
                #increasing cart_item quantity
                item = Cart_item.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = Cart_item.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()

        else:
            cart_item = Cart_item.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )

            cart_item.variations.clear()
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect('cart')



def remove_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = Cart_item.objects.get(product=product,cart=cart,id=cart_item_id)
    try:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()

    except:
        pass 

    return redirect('cart')


def delete_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = Cart_item.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


# Creating Checkout Functionality

@login_required(login_url='login')

def checkout(request,total=0,quantity=0,tax=0,grand_total=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = Cart_item.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (3 * total)/100
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'total' : total,
        'quantity' : quantity,
        'grand_total' : grand_total,
        'tax': tax,
    }


    return render(request,'store/checkout.html',context)


    


