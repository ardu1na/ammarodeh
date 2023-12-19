
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from products.views import cart, add_product_into_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Structure.urls')),
    path('products/', include('products.urls')),
    path('cart/', cart, name="cart"),
    path('cart/add/<int:product_id>', add_product_into_cart, name="add_product"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


