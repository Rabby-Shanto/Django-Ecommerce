import json
from django.shortcuts import render,redirect
from .models import Order,OrderedProduct,Payment
from cart.models import Cart_item
from .forms import OrderForm
import datetime


def payment(request):
    body =  json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    # storing transaction details
    payment = Payment(
        user = request.user,
        payment_id = body['transactionID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()

    order.payment = payment
    order.is_ordered = True #After payment successful,it should be true
    order.save()

    # move the cart item to ordered products table

    cart_item = Cart_item.objects.filter(user=request.user)
    for item in cart_item:
        ordered_product = OrderedProduct()
        ordered_product.order_id = order.id
        ordered_product.payment = payment
        ordered_product.user_id = request.user.id
        ordered_product.product_id = item.product_id
        ordered_product.quantity = item.quantity
        #variation isn't here because it is many to many field,so we can't use variation withour saving the ordered product
        ordered_product.product_price  = item.product.price
        ordered_product.is_ordered = True
        ordered_product.save()

        #starting to get variation 

        cart_item = Cart_item.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        ordered_product = OrderedProduct.objects.get(id = ordered_product.id)
        ordered_product.variations.set(product_variation)
        ordered_product.save()
        

    return render(request,'orders/payments.html')

def place_order(request,total=0,quantity=0):
    current_user = request.user

#    if cart count is =<0,redirect to store page

    cart_items = Cart_item.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0 :
        
        return redirect('store')

    grand_total = 0
    tax = 0


    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (3 * total)/100
    grand_total = tax + total

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user

            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            year = int(datetime.date.today().strftime('%Y'))
            day = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d = datetime.date(year,month,day)
            current_date = d.strftime("%Y%d%m")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)

            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
                
                }

            return render(request,'orders/payments.html',context)


    else:
        return redirect('checkout')






