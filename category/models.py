from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200,unique=True)
    category_img = models.ImageField(upload_to='photos/categories',blank=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.CharField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = 'categories'


# getting category wise product by clicking the category name

    def get_url(self):
        return reverse("Category_products",args = [self.slug])

    def __str__(self):
        return self.category_name

