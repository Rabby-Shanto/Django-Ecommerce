from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.CharField(max_length=500,blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('products_details',args=[self.category.slug,self.slug])


    def __str__(self):
        return self.product_name


variation_fields = (
    ('color','color'),
    ('size','size'),
)



# We are using variation manager to manage the variations in template so that colors won't get overwrite with sizes.We should make the selection pane for colors with their color and sizes with their size.

#.................... Variation Manager starts.......................

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_class = 'color',is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_class = 'size',is_active=True)

#...................End............................................... 


#.................Variation Model starts..................

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_class = models.CharField(max_length=100,choices=variation_fields)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

#.................End...........................................



