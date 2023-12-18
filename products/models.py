from django.contrib.auth.models import User
from django.db import models 

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(Category , related_name='products' , on_delete= models.CASCADE)
    name = models.CharField(max_length=255)
    descrption = models.TextField(blank=True , null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='product_image',blank=True,null=True)
    created_by = models.ForeignKey(User , related_name='products', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
       
    def __str__(self):
        return self.name

