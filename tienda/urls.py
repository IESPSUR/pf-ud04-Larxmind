from django.urls import path
from . import views

from tienda.views import Listado, ProductoCrear, ProductoDetalle, ProductoEliminar, ProductoActualizar

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),


    # La ruta 'listado productos' en donde se listan todos los registros de productos
    path('tienda/listado_productos', Listado.as_view(template_name="tienda/productos/listado_productos.html"),
         name='listado_productos'),

    # La ruta 'detalles' en donde mostraremos una página con los detalles de un producto
    path('tienda/detalle/<int:pk>', ProductoDetalle.as_view(template_name="tienda/productos/detalles.html"),
         name='detalles'),

    # La ruta 'crear' en donde mostraremos un formulario para crear un nuevo registro de producto
    path('tienda/crear', ProductoCrear.as_view(template_name="tienda/productos/crear.html"), name='crear'),

    # La ruta 'actualizar' en donde mostraremos un formulario para actualizar un registro de producto
    path('tienda/editar/<int:pk>', ProductoActualizar.as_view(template_name="tienda/productos/actualizar.html"),
         name='actualizar'),

    # La ruta 'eliminar' que usaremos para eliminar un postre o registro de la Base de Datos
    path('tienda/eliminar/<int:pk>', ProductoEliminar.as_view(), name='eliminar'),

    # Ruta para acceder al listado de compras
    path('tienda/listado_compra', views.listado_compra, name='listado_compra'),

    # Ruta para mostrar el producto de la compra
    path('tienda/comprar/<int:pk>', views.compra_producto, name='compra_producto'),

    # Ruta registro usuario
    path('tienda/registra_usuario', views.registro_usuario, name='registro_usuario'),

    # Ruta Logeo de usuario
    path('tienda/login_usuario', views.login_usuario, name='login_usuario'),

    # Ruta logout de usuario
    path('tienda/logout', views.logout_usuario, name='logout'),

    # Ruta para mostrar los difentes informes posibles
    path('tienda/informes', views.informes, name='informes'),

    # Ruta para mostrar un listado de las marcas
    path('tienda/informes/listado_por_marca', views.listar_por_marca, name='listado_por_marca'),

    # Ruta para mostrar los productos de una marca específica
    path('tienda/informes/listado_productos_por_marca/<str:nombre_marca>', views.listar_productos_marca,
         name='listado_productos_marca'),

    # Ruta para mostrar top 10 de los productos más vendidos
    path('tienda/informes/top_ten_productos', views.top_ten_productos, name='top_ten_productos'),

    path('tienda/informes/lista_usuarios', views.lista_usuarios, name='lista_usuarios'),

    path('tienda/informes/compras_usuario/<int:usuario>', views.compras_usuario, name='compras_usuario'),

    path('tienda/informes/top_ten_usuarios', views.top_ten_usuarios, name='top_ten_usuarios'),





]
