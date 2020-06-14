from django.urls import path
from .views import index, register, RegistrarPerfilCliente, logiar, UsuarioDetalle, RegistrarDireccion, RegistrarProducto, ListarProductos, EditarProducto, EliminarProducto

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
]