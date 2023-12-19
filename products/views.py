from django.shortcuts import render , get_object_or_404, redirect
from django.urls import reverse

from .models import Products, \
                    Cart, ProductCart

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



############################################


##########################
################################## Cart and shopping logic

#@api_view(['POST', 'GET'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def add_product_into_cart(request, product_id):
    client = request.user.client
    cart, created = Cart.objects.get_or_create(client=client, done=False)
    try:
        product = Products.objects.get(pk=product_id)
        product_cart, created = ProductCart.objects.get_or_create(cart=cart, product=product)
          
        return redirect('cart')
    
    except Products.DoesNotExist:
        context = {
            'error': 'Ups! Something gets wrong, please try again or contact the webmaster. Thanks!'
        }
        return redirect('home')

#@api_view(['DELETE'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def delete_cart_product(request, product_cart_id):
    product_cart = ProductCart.objects.filter(id=product_cart_id).first()
    if product_cart:
        product_cart.delete() ## AJAX HERE
        return redirect(reverse('cart')+ "?deleted")


#@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def cart(request):
    client = request.user.client
    try:
        cart = Cart.objects.get(client=client, done=False)
        context = {
            'cart' : cart,
            'client': client,
        }
        template_name = 'cart.html'
        return render(request, template_name, context)
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(client=client, done=False)
        context = {
            'cart' : cart,
            'client': client,
        }
        template_name = 'cart.html'
        return render(request, template_name, context)
    

#@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def checkout(request, cart_id):
    cart = Cart.objects.filter(id=cart_id, done=False).first()
    client = cart.client
    
    context = {
        'cart' : cart,
    }
    template_name = 'checkout.html'
    return render(request, template_name, context)
