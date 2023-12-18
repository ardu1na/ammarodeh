from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .forms import LoginForm
from django.contrib.auth import views as auth_views

app_name = ''  # This sets the app name/namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', include('products.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='structure/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)