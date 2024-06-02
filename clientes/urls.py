from django.urls import path
from . import views
from .views import PedidoWizard

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('productos/<int:producto_id>/', views.detalles_producto, name='detalles_producto'),
    path('productos/<int:producto_id>/realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido/', PedidoWizard.as_view(), name='pedido'),
]
