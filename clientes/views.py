# clientes/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .forms import SeleccionProductoForm, ConfirmacionPedidoForm, EleccionEntregaForm, PagoForm, RegistroForm
from .models import Producto, Pedido, Cliente
from formtools.wizard.views import SessionWizardView

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.set_password(form.cleaned_data['password'])
            cliente.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'clientes/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('productos')
        else:
            return render(request, 'clientes/login.html', {'error': 'Invalid credentials'})
    return render(request, 'clientes/login.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'clientes/productos.html', {'productos': productos})

def detalles_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'clientes/detalles_producto.html', {'producto': producto})

FORMS = [
    ('seleccion', SeleccionProductoForm),
    ('confirmacion', ConfirmacionPedidoForm),
    ('entrega', EleccionEntregaForm),
    ('pago', PagoForm)
]

TEMPLATES = {
    'seleccion': 'clientes/seleccion_producto.html',
    'confirmacion': 'clientes/confirmacion_pedido.html',
    'entrega': 'clientes/eleccion_entrega.html',
    'pago': 'clientes/pago.html'
}

class PedidoWizard(SessionWizardView):
    form_list = FORMS
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        datos = {key: form.cleaned_data for key, form in zip(FORMS, form_list)}
        pedido = Pedido(
            cliente=self.request.user,
            producto=datos['seleccion']['producto'],
            cantidad=datos['seleccion']['cantidad'],
            direccion=datos['confirmacion']['direccion'],
            telefono=datos['confirmacion']['telefono'],
            peticiones_especiales=datos['confirmacion']['peticiones_especiales'],
            tipo_entrega=datos['entrega']['tipo_entrega'],
            metodo_pago=datos['pago']['metodo_pago'],
            detalles_pago=datos['pago']['detalles_pago'],
        )
        pedido.save()
        return render(self.request, 'clientes/pedido_completado.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
