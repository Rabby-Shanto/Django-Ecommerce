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
# Create your views here.

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
                print("Entering try block")
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cartitem_exists = Cart_item.objects.filter(cart=cart).exists()
                print(is_cartitem_exists)
                if is_cartitem_exists:
                    cart_item = Cart_item.objects.filter(cart=cart)
                    print(cart_item)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                print("Entering Except block")
                pass
            auth.login(request,user)
            messages.success(request,'You are now logged in')
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

    return render(request,'accounts/dashboard.html')

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