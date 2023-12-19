from django.shortcuts import render , get_object_or_404, redirect
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
        context = {
            'cart': cart,
            'cart_product': product_cart,
            }
        template_name = 'cart.html'    
        return render(request, template_name, context)
    
    except Products.DoesNotExist:
        context = {
            'error': 'Ups! Something gets wrong, please try again or contact the webmaster. Thanks!'
        }
        return redirect('home')



#@api_view(['DELETE'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def delete_product_from_cart(request, product_id):
    client = request.user.client
    try:
       # Delete the product from the cart
        try:
            product_cart = ProductCart.objects.get(pk=product_id)
            cart = product_cart.cart
            if cart.client == client:
                product_cart.delete()
        except ProductCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        cart_serializer = CartSerializer(instance=cart)
        return Response({'cart': cart_serializer.data}, status=status.HTTP_200_OK)
    
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)




#@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def cart_detail(request):
    client = request.user.client
    try:
        cart = Cart.objects.get(client=client, done=False)
        cart_serializer = CartDetailSerializer(instance=cart)
        return Response({'cart':cart_serializer.data}, status=status.HTTP_200_OK)
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(client=client, done=False)
        cart_serializer = CartDetailSerializer(instance=cart)
        return Response({'cart':cart_serializer.data}, status=status.HTTP_200_OK)
    

