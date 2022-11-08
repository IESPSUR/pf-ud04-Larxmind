from django.shortcuts import render
from .models import Producto

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
    return render(request,'tienda/index.html', {})


def listado_productos(request):
    productos = Producto.objects.all()
    return render(request,'tienda/listado_productos.html', {'productos':productos})

class Listado(ListView):
    model = Producto # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'


class ProductoCrear(SuccessMessageMixin, CreateView):
    model = Producto  # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'
    form = Producto  # Definimos nuestro formulario con el nombre de la clase o modelo 'Producto'
    fields = "__all__"  # Le decimos a Django que muestre todos los campos de la tabla 'producto' de nuestra Base de Datos
    success_message = 'Producto Creado Correctamente !'  # Mostramos este Mensaje luego de Crear un Postre

    # Redireccionamos a la página principal luego de crear un registro o postre
    def get_success_url(self):
        return reverse('listado_productos')  # Redireccionamos a la vista principal 'leer'


class ProductoDetalle(DetailView):
    model = Producto # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'


class ProductoActualizar(SuccessMessageMixin, UpdateView):
    model = Producto  # Llamamos a la clase 'Producto' que se encuentra en nuestro archivo 'models.py'
    form = Producto  # Definimos nuestro formulario con el nombre de la clase o modelo 'Producto'
    fields = "__all__"  # Le decimos a Django que muestre todos los campos de la tabla 'producto' de nuestra Base de Datos
    success_message = 'Producto Actualizado Correctamente !'  # Mostramos este Mensaje luego de Editar un Postre

    # Redireccionamos a la página principal luego de actualizar un registro o postre
    def get_success_url(self):
        return reverse('listado_productos')  # Redireccionamos a la vista principal 'listado_productos'


class ProductoEliminar(SuccessMessageMixin, DeleteView):
    model = Producto
    form = Producto
    fields = "__all__"

    # Redireccionamos a la página principal luego de eliminar un registro o postre
    def get_success_url(self):
        success_message = 'Producto Eliminado Correctamente !'  # Mostramos este Mensaje luego de Editar un Producto
        messages.success(self.request, (success_message))
        return reverse('listado_productos')  # Redireccionamos a la vista principal 'listado_productos'#


