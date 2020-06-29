from django.urls import path
from .views import index, register, RegistrarPerfilCliente, RegistrarPerfilProveedor, logiar, RegistrarDireccion, RegistrarProducto, ListarProductos, EditarProducto, EliminarProducto
from .views import RegistrarVenta, ListarVenta
from .views import ListarCesta, Agregar_a_Cesta, ActualizarCesta
from .views import ListarSubCategoria
from .views import UsuarioDetalle, EditarInformacionPerfilCliente,EditarInformacionPerfilProveedor, EditarDireccion, ListarDireccion, EliminarDireccion
from .views import logout_user
app_name='tienda'
urlpatterns=[
    path('', index.as_view(), name='index'),
    path('perfil_info/<int:pk>/<str:tipo_usuario>',UsuarioDetalle.as_view(), name='infoUsuario'),
    path('perfil_info/editar_cliente/<int:pk>', EditarInformacionPerfilCliente.as_view(), name='editarUsuario'),#pk es el ID del perfil
    path('perfil_info/editar_provee/<int:pk>', EditarInformacionPerfilProveedor.as_view(), name="editarProveedor"),
    path('registrar', register, name='registrar'),
    path('registrar/perfil_clien/<int:pk>', RegistrarPerfilCliente, name='perfil'),
    path('registrar/perfil_provee/<int:pk>',RegistrarPerfilProveedor, name='reg_provee'),
    path('login', logiar, name='login'),
    path('logout', logout_user, name='logout'),
    path('registrar/direccion/<int:pk>', ListarDireccion.as_view(), name='dire_list'),
    path('registrar/direccion/reg_dire/<int:pk>', RegistrarDireccion.as_view(), name='dire'),#pk seria el id de el cliente al que se le va registrar la direccion
    path('registrar/direccion/editar_dire/<int:pk>', EditarDireccion.as_view(), name='dire_edi'),#pk seria el id de la direccion que se quiere editar
    path('registrar/direccion/eliminar_dire/<int:pk>', EliminarDireccion.as_view(), name='del_dire'),#pk el id de la direccion que se desea eliminar
    path('producto/<int:pk>', ListarProductos.as_view(), name='listar_prod'), # el pk es el id del proveedor que esta viendo su listado de productos registrados
    path('producto/editar_producto/<int:pk>',EditarProducto.as_view(), name='edit_prod'),#el pk hace referencia al id del producto que se va a editar
    path('producto/guardar_producto/<int:pk>', RegistrarProducto.as_view(), name='prod'),#el pk argumento hace referencia al id del mayorista que esta guardando su producto
    path('producto/eliminar_producto/<int:pk>', EliminarProducto.as_view(), name='del_prod'),
    path('venta/registrar_venta/<int:pk>/<int:pk1>/<str:precio>', RegistrarVenta.as_view(), name='reg_venta'),#pk es el id de cliente que relizara la compra
    path('venta/<int:pk>', ListarVenta.as_view(), name='list_venta'),#pk es el id del cliente que realiza la venta y el pk2 es el id del producto a comprar
    path('cesta/<int:pk>', ListarCesta.as_view(), name='list_cesta'),#pk es el id del cliente al que esta asociada la cesta
    path('cesta/agregar_cesta/<int:pk>',Agregar_a_Cesta.as_view(), name='agregar_cesta'),#pk es el id del cliente asociado a la cesta
    path('cesta/actualizar_cesta/<int:pk>', ActualizarCesta.as_view(), name='actualizar_cesta'),#pk recive el id de la cesta a editar
    path('sub_categoria/<int:pk>', ListarSubCategoria.as_view(), name='sub_categoria'), #pk seria el valor de la Categia padre
]
