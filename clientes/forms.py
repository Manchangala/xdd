from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente

class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password1', 'password2']




from .models import Pedido, Producto, Cliente

class SeleccionProductoForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), required=True)
    cantidad = forms.IntegerField(min_value=1, required=True)

class ConfirmacionPedidoForm(forms.Form):
    direccion = forms.CharField(max_length=100, required=True)
    telefono = forms.CharField(max_length=20, required=True)
    peticiones_especiales = forms.CharField(widget=forms.Textarea, required=False)


class EleccionEntregaForm(forms.Form):
    opciones_entrega = [
        ('recoger', 'Recoger en tienda'),
        ('domicilio', 'Entrega a domicilio'),
    ]
    tipo_entrega = forms.ChoiceField(choices=opciones_entrega, required=True)

class PagoForm(forms.Form):
    metodo_pago = forms.CharField(max_length=100, required=True)
    detalles_pago = forms.CharField(widget=forms.Textarea, required=False)

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password', 'nombre', 'direccion', 'telefono']

