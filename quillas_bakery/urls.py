from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from clientes import views as cliente_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', cliente_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='clientes/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='clientes/logout.html'), name='logout'),
    path('productos/', cliente_views.productos, name='productos'),  # Nueva vista de productos
    path('', include('clientes.urls')),  # Incluir las URLs de la app de clientes
]
