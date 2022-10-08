from pyexpat import model
from django import forms
from .models import ReviewRating


class ReviewForm(forms.ModelForm):
    model = ReviewRating
    fields = ['subject','user','review','rating']