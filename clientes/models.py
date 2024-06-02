# clientes/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class Cliente(AbstractUser):
    nombre = models.CharField(max_length=100, default='default_nombre')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    codigo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    direccion = models.CharField(max_length=100, default='default_direccion')
    telefono = models.CharField(max_length=20, default='0000000000')
    peticiones_especiales = models.TextField(blank=True, null=True)
    tipo_entrega = models.CharField(max_length=50, default='recoger')
    metodo_pago = models.CharField(max_length=100)
    detalles_pago = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):
        return f"Pedido {self.id} de {self.cliente.nombre}"
