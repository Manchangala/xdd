from django.db import models
from django.contrib.auth.models import AbstractUser

class Cliente(AbstractUser):
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    # Puedes agregar más campos si es necesario

    def __str__(self):
        return self.username

class Producto(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_PEDIDO_CHOICES = (
        ('P', 'Pendiente'),
        ('C', 'Completado'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    peticiones_especiales = models.TextField(blank=True, null=True)
    entrega = models.CharField(max_length=50, choices=[('D', 'Domicilio'), ('R', 'Recogida en tienda')])
    metodo_pago = models.CharField(max_length=50, choices=[('E', 'Efectivo'), ('T', 'Tarjeta')])
    estado = models.CharField(max_length=1, choices=ESTADO_PEDIDO_CHOICES, default='P')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.id} de {self.cliente.username}"
