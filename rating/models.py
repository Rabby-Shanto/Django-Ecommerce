
from django.db import models
from store.models import *
from User.models import UserAcc

# Create your models here.

class ReviewRating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(UserAcc,on_delete=models.CASCADE)
    subject = models.CharField(max_length=500,blank=True)
    review = models.CharField(max_length=500,default=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 

        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.subject
