from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Pedido
from .forms import SeleccionProductoForm, ConfirmacionPedidoForm, EleccionEntregaForm, PagoForm, RegistroForm
from django.contrib.auth import login, authenticate

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

