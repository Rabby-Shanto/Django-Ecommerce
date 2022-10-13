from multiprocessing import context
from sqlite3 import paramstyle
from django.shortcuts import render,redirect
from django.http import HttpResponse
from User.models import UserAcc
from cart.models import Cart,Cart_item
from .forms import RegistrationForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#verification mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
#....
from cart.views import _cart_id
import requests
# Create your views here.
from order.models import Order
#Registreation and Sending Email verification to user email

def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = UserAcc.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number= phone_number
            user.save()
            # User Activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/verification_mail.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request,"Registration Successful")
            return redirect('/accounts/login/?command=verification&email='+email)


    else:

        form = RegistrationForm()

    context = {

        'form': form,
        }

    return render(request,'accounts/register.html',context)


#User Login Functionality

def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST.get('password')

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cartitem_exists = Cart_item.objects.filter(cart=cart).exists()
                # Getting the product variation

                if is_cartitem_exists:
                    cart_item = Cart_item.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                        # Get the cart item from the user to access product variation
                    cart_item = Cart_item.objects.filter(user = user)
                    ex_variation_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_variation_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_variation_list:
                            index = ex_variation_list.index(pr)
                            item_id = id[index]
                            item = Cart_item.objects.get(id=item_id)
                            item.quantity += 1
                            item.user=user
                            item.save()
                        else:
                            cart_item = Cart_item.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print(query)
                params = dict(x.split("=") for x in query.split('&'))
                print(params)
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
                
            except:
                
                return redirect('dashboard')

        else:
            messages.error(request,'Invalid email or password!')
            return redirect('login')


    return render(request,'accounts/login.html')



@login_required(login_url='login')

def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")

    return redirect('login')


# Account activation through Email 

def activate(request,uidb64,token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAcc._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,UserAcc.DoesNotExist):

        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Congrats,Your account is activated")

        return redirect('login')
    else:
        messages.error(request,"Invalid Link!Please try again")

        return redirect('register')


# Dashboard View

@login_required(login_url='login')

def dashboard(request):

    orders = Order.objects.order_by('created_at').filter(user_id = request.user.id,is_ordered=True)
    orders_count = orders.count()
    context = {
        'orders_count' : orders_count,
    }
    return render(request,'accounts/dashboard.html',context)

# Forget password

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if UserAcc.objects.filter(email=email).exists():
            user = UserAcc.objects.get(email__exact=email)


            # Reset forgotten Password

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password_activation.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'password reset mail has been sent to your email!')

            return redirect('login')

        else:
            messages.error(request,"Account doesn't exist")
            return redirect('forgotpassword')

    else:

        return render(request,'accounts/forgotpassword.html')



def resetpass_activate(request,uidb64,token):



    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAcc._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,UserAcc.DoesNotExist):

        user = None

    if user is not None and default_token_generator.check_token(user,token):

        request.session['uid'] = uid
        messages.success(request,"please reset your password")

        return redirect('reset_password')

    else:

        messages.error(request,"Link expired!")
        return redirect('login')


def reset_password(request):

    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]


        if password == confirm_password:
            uid = request.session.get('uid')
            user = UserAcc.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful!')
            return redirect('login')

        else:
            messages.error(request,"password doesn't match!")  
            return redirect('reset_password')

    else:

        return render(request,'accounts/reset_password.html')



def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context ={
        'orders' : orders
    }
    return render(request,'accounts/my_order.html',context)