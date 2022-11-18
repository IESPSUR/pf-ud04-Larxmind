from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Producto, CheckOutForm, Compra

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Nos sirve para redireccionar después de una acción revirtiendo patrones de expresiones regulares
from django.urls import reverse

# Habilitamos el uso de mensajes en Django
from django.contrib import messages

# Habilitamos los mensajes para class-based views
from django.contrib.messages.views import SuccessMessageMixin

# Habilitamos los formularios en Django
from django import forms

# Create your views here.


def welcome(request):
    return render(request, 'tienda/index.html', {})

# LISTA Y EDICIÓN DE PRODUCTOS-_____________________________________________________________________
def listado_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/listado_productos.html', {'productos': productos})


class Listado(ListView):
    model = Producto  # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'


class ProductoCrear(SuccessMessageMixin, CreateView):
    model = Producto  # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'
    form = Producto  # Definimos nuestro formulario con el nombre de la clase o modelo 'Producto'
    fields = "__all__"  # Muestra todos los campos de la tabla 'producto' de nuestra Base de Datos
    success_message = 'Producto Creado Correctamente !'  # Mostramos este Mensaje luego de Crear un Postre

    # Redireccionamos a la página principal luego de crear un registro o postre
    def get_success_url(self):
        return reverse('listado_productos')  # Redireccionamos a la vista principal 'leer'


class ProductoDetalle(DetailView):
    model = Producto  # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'


class ProductoActualizar(SuccessMessageMixin, UpdateView):
    model = Producto  # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'
    form = Producto  # Definimos nuestro formulario con el nombre de la clase o modelo 'Producto'
    fields = "__all__"  # muestra todos los campos de la tabla 'producto' de nuestra Base de Datos
    success_message = 'Producto Actualizado Correctamente !'  # Mostramos este Mensaje luego de Editar un Postre

    # Redireccionamos a la página principal luego de actualizar un registro o postre
    def get_success_url(self):
        return reverse('listado_productos')  # Redireccionamos a la vista principal 'listado_productos'


class ProductoEliminar(SuccessMessageMixin, DeleteView):
    model = Producto
    form = Producto
    fields = "__all__"

    # Redireccionamos a la página principal luego de eliminar un registro
    def get_success_url(self):
        success_message = 'Producto Eliminado Correctamente !'  # Mostramos este Mensaje luego de Editar un Producto
        messages.success(self.request, success_message)
        return reverse('listado_productos')  # Redireccionamos a la vista principal 'listado_productos'#


# COMPRA ____________________________________________________________________________________

def listado_compra(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/listado_compra.html', {'productos': productos})


def compra_producto(request, pk):
    form = CheckOutForm()
    producto = get_object_or_404(Producto, pk=pk)
    productos = Producto.objects.all()


    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                nombre_usuario = request.user.id
            else:
                nombre_usuario = None
            # Obtención de las unidades del formulario compra_producto
            cantidad_requerida = form.cleaned_data['cantidad_requerida']

            if cantidad_requerida > producto.unidades:
                messages.add_message(request, messages.INFO, 'Unidades disponibles menor que las pedidas.')

            else:
                producto.unidades -= cantidad_requerida
                producto.save()
                Compra.objects.create(producto=producto.nombre, fecha=timezone.now(), unidades=producto.unidades,
                                      importe=producto.precio * cantidad_requerida, usuario_id=nombre_usuario)
                messages.add_message(request, messages.INFO, 'Producto comprado con éxito')

        return redirect('listado_compra')
    else:
        return render(request, 'tienda/comprar.html', {'form': form, 'producto': producto, 'pk':pk})

#CREAR USUARIOS __________________________________________________________________________________________-

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Registro completado")
            return redirect('welcome')
        messages.error(request, "Registro no completado")
    form = UserCreationForm()
    return render(request, 'tienda/registro_usuario.html', {'formulario_registro': form})


def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password = password)

            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenido")
                return redirect('welcome')
            else:
                messages.error(request, "Error al autenticarse")
        else:
            messages.error(request, "Error al autenticarse")
    form = AuthenticationForm()
    return render(request, 'tienda/login_usuario.html', {'formulario_login': form})


def logout_usuario(request):
    logout(request)
    messages.info(request, "Hasta luego")
    return redirect('welcome')


