from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente

class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password1', 'password2']


from .models import Pedido, Producto, Cliente

class SeleccionProductoForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    cantidades = forms.CharField(widget=forms.HiddenInput(), required=True)

class ConfirmacionPedidoForm(forms.Form):
    direccion = forms.CharField(max_length=255, required=True)
    telefono = forms.CharField(maxlength=20, required=True)
    peticiones_especiales = forms.CharField(widget=forms.Textarea, required=False)


class EleccionEntregaForm(forms.Form):
    OPCIONES_ENTREGA = [
        ('recoger', 'Recoger en tienda'),
        ('entrega', 'Entrega a domicilio')
    ]
    recogida_entrega = forms.ChoiceField(choices=OPCIONES_ENTREGA, required=True)

class PagoForm(forms.Form):
    metodo_pago = forms.ChoiceField(
        choices=[('tarjeta', 'Tarjeta de Crédito/Débito'), ('efectivo', 'Efectivo')],
        required=True
    )
    numero_tarjeta = forms.CharField(max_length=16, required=False)
    nombre_titular = forms.CharField(max_length=100, required=False)
    cvv = forms.CharField(max_length=3, required=False)
    fecha_expiracion = forms.DateField(required=False)

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['username', 'password', 'direccion', 'telefono']
        widgets = {
            'password': forms.PasswordInput(),
        }
