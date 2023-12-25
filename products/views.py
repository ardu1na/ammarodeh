from django.shortcuts import render , get_object_or_404, redirect
from django.urls import reverse
from products.forms import ClientForm, CartForm
from .models import Products, \
                    Cart, ProductCart, Client, Order


############################################
from collections import defaultdict

def get_client_transactions(request, client_id):
    client = Client.objects.filter(id=client_id).first()
    transactions = Order.objects.filter(cart__client=client)

    transactions_by_category = defaultdict(list)

    for transaction in transactions:
        cart = transaction.cart
        for product_cart in cart.products.all():
            category = product_cart.product.category 
            transactions_by_category[category].append(transaction)

    for category, category_transactions in transactions_by_category.items():
     
        print(f"Table for {category} transactions:")
        print("Transaction ID\tProduct")
        for transaction in category_transactions:
            for product_cart in transaction.cart.products.all():
                print(f"{transaction.id}\t{product_cart.product.name}\t")
        print("\n")



############################################

def detail (request , pk) :
    product = get_object_or_404(Products , pk=pk)
    related_products = Products.objects.filter(category=product.category).exclude(pk=pk)[0:3]

    return render(request, 'Products/detail.html' , {

         'product' : product ,
         'related_products' : related_products ,
    })


def product_list(request):
    products = Products.objects.all()  
    return render(request, 'structure/test_page.html', {'products': products})



############################################


##########################
################################## Cart and shopping logic

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

def delete_cart_product(request, product_cart_id):
    product_cart = ProductCart.objects.filter(id=product_cart_id).first()
    if product_cart:
        product_cart.delete() ## AJAX HERE
    return redirect(reverse('cart')+ "?deleted")


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
    
def checkout(request, cart_id):
    cart = Cart.objects.filter(id=cart_id).first()
    if request.method == 'GET':
        client_form = ClientForm(instance=cart.client)
        cart_form = CartForm(instance=cart)
        context = {
        'cart' : cart,
        'client_form': client_form,
        'cart_form': cart_form,
        }

        template_name = 'checkout.html'
        return render(request, template_name, context)
    if request.method == 'POST':
        if 'client_form' in request.POST:
            client_form = ClientForm(request.POST, instance=cart.client)
            if client_form.is_valid():
                updated_client = client_form.save()
        if 'cart_form' in request.POST: # this is for checking the payment id submited by client bf close order 
            cart_form = CartForm(request.POST, instance=cart)
            if cart_form.is_valid():
                updated_cart = cart_form.save()
                updated_cart.done = True
                updated_cart.save()
        return redirect('checkout', cart.id)
    
