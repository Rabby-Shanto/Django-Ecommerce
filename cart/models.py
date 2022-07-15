from django.db import models
from store.models import Product, Variation
from User.models import UserAcc

# Create your models here.

class Cart(models.Model):

    cart_id = models.CharField(max_length=200,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cart_id


class Cart_item(models.Model):

    user = models.ForeignKey(UserAcc,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):

        return self.product.price * self.quantity

    class Meta:
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return self.product.product_name

