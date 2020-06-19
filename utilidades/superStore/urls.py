from django.urls import path
from .views import index, register, RegistrarPerfilCliente, logiar, UsuarioDetalle, RegistrarDireccion, RegistrarProducto, ListarProductos, EditarProducto, EliminarProducto
from .views import RegistrarVenta, ListarVenta
from .views import ListarCesta, Agregar_a_Cesta, ActualizarCesta
from .views import ListarSubCategoria
app_name='tienda'
urlpatterns=[
    path('', index.as_view(), name='index'),
    path('registrar', register, name='registrar'),
    path('registrar/perfil_reg/<str:username>/<str:tipo_usuario>', RegistrarPerfilCliente, name='perfil'),
    path('login', logiar, name='login'),
    path('perfil_info/<int:pk>/<str:tipo_usuario>',UsuarioDetalle.as_view(), name='infoUsuario'),
    path('registrar/direccion/<int:pk>',RegistrarDireccion.as_view(), name='dire'),
    path('producto/<int:pk>', ListarProductos.as_view(), name='listar_prod'), # el pk es el id del proveedor que esta viendo su listado de productos registrados
    path('producto/editar_producto/<int:pk>',EditarProducto.as_view(), name='edit_prod'),#el pk hace referencia al id del producto que se va a editar
    path('producto/guardar_producto/<int:pk>', RegistrarProducto.as_view(), name='prod'),#el pk argumento hace referencia al id del mayorista que esta guardando su producto
    path('producto/eliminar_producto/<int:pk>', EliminarProducto.as_view(), name='del_prod'),
    path('venta/registrar_venta/<int:pk>', RegistrarVenta.as_view(), name='reg_venta'),#pk es el id de cliente que relizara la compra
    path('venta/<int:pk>', ListarVenta.as_view(), name='list_venta'),#pk es el id del proveedor al que se le muestran todos sus productos
    path('cesta/<int:pk>', ListarCesta.as_view(), name='list_cesta'),#pk es el id del cliente al que esta asociada la cesta
    path('cesta/agregar_cesta/<int:pk>',Agregar_a_Cesta.as_view(), name='agregar_cesta'),#pk es el id del cliente asociado a la cesta
    path('cesta/actualizar_cesta/<int:pk>', ActualizarCesta.as_view(), name='actualizar_cesta'),#pk recive el id de la cesta a editar
    path('sub_categoria/<int:pk>', ListarSubCategoria.as_view(), name='sub_categoria'), #pk seria el valor de la Categia padre
]
