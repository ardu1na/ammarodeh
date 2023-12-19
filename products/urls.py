from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('<int:pk>/' , views.detail ,name='detail') ,
    path('product_list/', views.product_list, name="product_list"), 
    path('cart/add/<int:product_id>/', views.add_product_into_cart, name="add_product"), 

]