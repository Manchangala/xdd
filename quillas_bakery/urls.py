# quillas_bakery/urls.py

from django.contrib import admin
from django.urls import path
from clientes import views as cliente_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', cliente_views.register, name='register'),
    path('login/', cliente_views.login_view, name='login'),
    path('productos/', cliente_views.productos, name='productos'),
    path('producto/<int:producto_id>/', cliente_views.detalles_producto, name='detalles_producto'),
    path('pedido/', cliente_views.PedidoWizard.as_view(), name='realizar_pedido'),
]
