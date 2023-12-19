from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/' , views.detail ,name='product_detail') ,
    path('', views.product_list, name="product_list"), 

]