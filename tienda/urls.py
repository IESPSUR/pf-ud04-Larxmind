from django.urls import path
from . import views

from tienda.views import Listado, ProductoCrear, ProductoDetalle, ProductoEliminar, ProductoActualizar

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/listado_productos', views.listado_productos, name='listado_productos'),

    # La ruta 'leer' en donde listamos todos los registros
    path('tienda/listado_productos', Listado.as_view(template_name="tienda/listado_productos.html"),
         name='listado_productos'),

    # La ruta 'detalles' en donde mostraremos una página con los detalles de un postre o registro
    path('tienda/detalle/<int:pk>', ProductoDetalle.as_view(template_name="tienda/detalles.html"), name='detalles'),

    # La ruta 'crear' en donde mostraremos un formulario para crear un nuevo postre o registro
    path('tienda/crear', ProductoCrear.as_view(template_name="tienda/crear.html"), name='crear'),

    # La ruta 'actualizar' en donde mostraremos un formulario para actualizar un postre o registro de la Base de Datos
    path('tienda/editar/<int:pk>', ProductoActualizar.as_view(template_name="tienda/actualizar.html"),
         name='actualizar'),

    # La ruta 'eliminar' que usaremos para eliminar un postre o registro de la Base de Datos
    path('tienda/eliminar/<int:pk>', ProductoEliminar.as_view(), name='eliminar'),
]
