from django.urls import path
from .views import index, register, RegistrarPerfilCliente, logiar, UsuarioDetalle, RegistrarDireccion, RegistrarProducto, ListarProductos

app_name='tienda'
urlpatterns=[
    path('', index.as_view(), name='index'),
    path('registrar', register, name='registrar'),
    path('registrar/perfil_reg/<str:username>/<str:tipo_usuario>', RegistrarPerfilCliente, name='perfil'),
    path('login', logiar, name='login'),
    path('perfil_info/<int:pk>/<str:tipo_usuario>',UsuarioDetalle.as_view(), name='infoUsuario'),
    path('registrar/direccion/<int:pk>',RegistrarDireccion.as_view(), name='dire'),
    path('producto/guardar_producto', RegistrarProducto.as_view(), name='prod'),
    path('producto', ListarProductos.as_view(), name='listar_prod')
]