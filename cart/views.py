from django.shortcuts import render,redirect
from .models import Cart,Cart_item

from store.models import Product

# Create your views here.




def cart(request,total=0,quantity=0,cart_items=None):

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = Cart_item.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

    except ObjectNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'total' : total,
        'quantity' : quantity
    }

    return render(request,'store/cart.html',context)



def _cart_id(request):

    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request,product_id):
     product = Product.objects.get(id=product_id) #fetch the product base on id
     try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
         #to get the cart using cart id present in session
     except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

     cart.save()

     try:
        cart_item = Cart_item.objects.get(product=product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
     except Cart_item.DoesNotExist:
        cart_item = Cart_item.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
     return redirect('cart')

    


