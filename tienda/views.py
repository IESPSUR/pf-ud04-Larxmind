from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Producto, CheckOutForm, Compra, Marca
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Nos sirve para redireccionar después de una acción revirtiendo patrones de expresiones regulares
from django.urls import reverse

# Habilitamos el uso de mensajes en Django
from django.contrib import messages

# Habilitamos los mensajes para class-based views
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.


def welcome(request):
    return render(request, 'tienda/index.html', {})


# LISTA Y EDICIÓN DE PRODUCTOS-_____________________________________________________________________
#  def listado_productos(request):
#    productos = Producto.objects.all()
#    return render(request, 'tienda/listado_productos.html', {'productos': productos})


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
    peticion_buscar = request.POST.get('buscar', '')  # obtención de input buscar
    productos = Producto.objects.all()  # obtención de todos los atributos de la clase prodcuto

    # en caso de recibir una petición de buscar, reasignación de valor a productos (salida)
    if peticion_buscar:
        productos = Producto.objects.filter(
            Q(nombre__icontains=peticion_buscar) |
            Q(marca__nombre__icontains=peticion_buscar) |
            Q(modelo__icontains=peticion_buscar)
        ).distinct()
    return render(request, 'tienda/productos/listado_compra.html', {'productos': productos})


def compra_producto(request, pk):
    form = CheckOutForm()
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            # En caso de formulario válido, comprobamos si el usuario está atentificado
            if request.user.is_authenticated:
                nombre_usuario = request.user.id
            else:
                nombre_usuario = None
            # Obtención de unidades_disponibles del formulario compra_producto
            cantidad_requerida = form.cleaned_data['cantidad_requerida']
            # comprobación de unidades suficientes antes de realizar pedido
            if cantidad_requerida > producto.unidades_disponibles:
                messages.add_message(request, messages.INFO, 'Unidades disponibles menor que las pedidas.')

            else:
                producto.unidades_disponibles -= cantidad_requerida
                producto.save()
                Compra.objects.create(producto=producto, fecha=timezone.now(), unidades_solicitadas=cantidad_requerida,
                                      importe=producto.precio * cantidad_requerida, usuario_id=nombre_usuario)
                messages.add_message(request, messages.INFO, 'Producto comprado con éxito')

        return redirect('listado_compra')
    else:
        return render(request, 'tienda/productos/comprar.html', {'form': form, 'producto': producto, 'pk': pk})


# CREAR USUARIOS __________________________________________________________________________________________

#  método para registrar un usuario en el sistema
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # formulario ofrecido por django para creacion de usuarios
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Registro completado")
            return redirect('welcome')
        messages.error(request, "Registro no completado")
    form = UserCreationForm()
    return render(request, 'tienda/usuarios/registro_usuario.html', {'formulario_registro': form})


#  método para registrar un usuario en el sistema
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # formulario de identification ofrecido por django
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenido")
                return redirect('welcome')
            else:
                messages.error(request, "Error al autenticarse")
        else:
            messages.error(request, "Error al autenticarse")
    form = AuthenticationForm()
    return render(request, 'tienda/usuarios/login_usuario.html', {'formulario_login': form})


def logout_usuario(request):
    logout(request)
    messages.info(request, "Hasta luego")
    return redirect('welcome')


# INFORMES _______________________________________________________________________________

def informes(request):
    return render(request, 'tienda/informes/informes.html')


#  Método para listar Marcas dentro de la BB DD
def listar_por_marca(request):
    # = (Producto.objects.values('marca').order_by())
    marcas = Marca.objects.all().values()
    listado_por_marca = list(marcas)

    return render(request, 'tienda/informes/listado_marcas.html', {'listado_por_marca': listado_por_marca})


#  Método para listar los productos enlazados a una marca en particular dentro de la BB DD
def listar_productos_marca(request, nombre_marca):
    listado_productos_marca = Producto.objects.filter(marca__nombre__icontains=nombre_marca).values()
    marca = nombre_marca
    return render(request, 'tienda/informes/listado_productos_por_marca.html',
                           {'listado_productos_marca': listado_productos_marca, 'marca': marca})


# Método para listar los 10 productos más vendidos
def top_ten_productos(request):
    lis_top_ten_productos = Compra.objects.values('producto__nombre', 'producto__modelo').annotate(
        total_unidades_vendidas=Sum('unidades_solicitadas')).order_by('-total_unidades_vendidas')[:10]
    listado_top_ten_productos = list(lis_top_ten_productos)
    return render(request, 'tienda/informes/top_ten_productos.html', {'listado_top_ten_productos':
                                                                      listado_top_ten_productos})


# Método para listar usuarios registrados
def lista_usuarios(request):
    listado_usuarios = User.objects.values('username', 'id')
    return render(request, 'tienda/informes/lista_usuarios.html', {'listado_usuarios': listado_usuarios})


# Método para listar compras realizadas por un usuario
def compras_usuario(request, usuario):
    lista_compras_usuario = Compra.objects.filter(usuario=usuario).values()
    user = User.objects.values('username').filter(id=usuario)
    return render(request, 'tienda/informes/compras_usuario.html', {'listado_compras_usuario': lista_compras_usuario,
                                                                    'usuario': user})


# Método para listar los 10 usuarios con mayores gastos
def top_ten_usuarios(request):
    listado_top_usuarios = User.objects.values('username').annotate(importe_total_compras=(Sum('compra__importe'))
                                                                    ).order_by('-importe_total_compras')[:10]

    return render(request, 'tienda/informes/listado_top_ten_usuarios.html', {'listado_top_ten_usuarios':
                                                                             listado_top_usuarios})
