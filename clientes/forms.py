from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente

class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password1', 'password2']


from .models import Pedido, Producto, Cliente

class SeleccionProductoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ConfirmacionPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['peticiones_especiales']
        widgets = {
            'peticiones_especiales': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EleccionEntregaForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['entrega']
        widgets = {
            'entrega': forms.Select(attrs={'class': 'form-control'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['metodo_pago']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }

class RegistroForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=True)
    telefono = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Cliente
        fields = ('username', 'direccion', 'telefono', 'password1', 'password2')
