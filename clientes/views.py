from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Pedido
from .forms import SeleccionProductoForm, ConfirmacionPedidoForm, EleccionEntregaForm, PagoForm, RegistroForm
from django.contrib.auth import login, authenticate
# clientes/views.py

from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from .forms import SeleccionProductoForm, ConfirmacionPedidoForm, RecogerODomicilioForm, PagoForm

FORMS = [
    ("seleccion", SeleccionProductoForm),
    ("confirmacion", ConfirmacionPedidoForm),
    ("metodo_entrega", RecogerODomicilioForm),
    ("pago", PagoForm)
]

TEMPLATES = {
    "seleccion": "clientes/seleccion_producto.html",
    "confirmacion": "clientes/confirmacion_pedido.html",
    "metodo_entrega": "clientes/metodo_entrega.html",
    "pago": "clientes/pago.html"
}

from .models import Pedido, Producto, Cliente

class PedidoWizard(SessionWizardView):
    template_name = "clientes/pedido_wizard.html"
    
    def done(self, form_list, **kwargs):
        # Recopilar datos del formulario
        form_data = [form.cleaned_data for form in form_list]
        
        # Extraer datos del formulario
        productos_data = form_data[0]['productos']
        cantidades_data = form_data[0]['cantidades']
        direccion = form_data[1]['direccion']
        telefono = form_data[1]['telefono']
        recogida_entrega = form_data[2]['recogida_entrega']
        peticiones_especiales = form_data[1]['peticiones_especiales']
        
        # Obtener el cliente actual
        cliente = Cliente.objects.get(user=self.request.user)
        
        # Crear el pedido
        pedido = Pedido(
            cliente=cliente,
            direccion=direccion,
            telefono=telefono,
            recogida_entrega=recogida_entrega,
            peticiones_especiales=peticiones_especiales,
            estado='pendiente'
        )
        pedido.save()
        
        # Agregar productos al pedido
        for producto_id, cantidad in zip(productos_data, cantidades_data):
            producto = Producto.objects.get(id=producto_id)
            pedido.productos.add(producto, through_defaults={'cantidad': cantidad})
        
        return render(self.request, 'clientes/pedido_completado.html', {
            'form_data': form_data,
            'pedido': pedido
        })


def home(request):
    return render(request, 'clientes/home.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'clientes/productos.html', {'productos': productos})

def detalles_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'clientes/detalles_producto.html', {'producto': producto})

def realizar_pedido(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        seleccion_form = SeleccionProductoForm(request.POST)
        confirmacion_form = ConfirmacionPedidoForm(request.POST)
        entrega_form = EleccionEntregaForm(request.POST)
        pago_form = PagoForm(request.POST)

        if seleccion_form.is_valid() and confirmacion_form.is_valid() and entrega_form.is_valid() and pago_form.is_valid():
            pedido = seleccion_form.save(commit=False)
            pedido.cliente = request.user
            pedido.producto = producto
            pedido.peticiones_especiales = confirmacion_form.cleaned_data['peticiones_especiales']
            pedido.entrega = entrega_form.cleaned_data['entrega']
            pedido.metodo_pago = pago_form.cleaned_data['metodo_pago']
            pedido.save()
            return redirect('productos')
    else:
        seleccion_form = SeleccionProductoForm(initial={'producto': producto})
        confirmacion_form = ConfirmacionPedidoForm()
        entrega_form = EleccionEntregaForm()
        pago_form = PagoForm()

    context = {
        'producto': producto,
        'seleccion_form': seleccion_form,
        'confirmacion_form': confirmacion_form,
        'entrega_form': entrega_form,
        'pago_form': pago_form,
    }
    return render(request, 'clientes/realizar_pedido.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('productos')
    else:
        form = RegistroForm()
    return render(request, 'clientes/register.html', {'form': form})

