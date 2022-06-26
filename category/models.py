from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200,unique=True)
    category_img = models.ImageField(upload_to='photos/categories',blank=True)
    slug = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        self.category_name

