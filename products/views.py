from django.shortcuts import render , get_object_or_404
from .models import Products

def detail (request , pk) :
    product = get_object_or_404(Products , pk=pk)
    related_products = Products.objects.filter(category=product.category).exclude(pk=pk)[0:3]




    return render(request, 'Products/detail.html' , {

         'product' : product ,
         'related_products' : related_products ,
    })
def product_list(request):
    products = Products.objects.all()  # Assuming you have a Product model
    return render(request, 'structure/test_page.html', {'products': products})
