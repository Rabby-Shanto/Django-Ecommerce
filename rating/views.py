from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from store.views import *
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages

# Create your views here.

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method=="POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,"Thank You! Your review has been updated.")
            return redirect(url)


        except:

            pass

