from django.urls import path, include
from .views import index, register, RegistrarPerfilCliente, RegistrarPerfilProveedor, logiar, RegistrarDireccion
from .views import RegistrarProducto, ListarProductos, EditarProducto, EliminarProducto, DetalleProducto, buscar_producto_tienda, cargar_todos_productos_tienda
from .views import RegistrarVenta, ListarVenta
from .views import ListarCesta, Agregar_a_Cesta, ActualizarCesta, EliminarCesta
from .views import ListarSubCategoria
from .views import UsuarioDetalle, EditarInformacionPerfilCliente,EditarInformacionPerfilProveedor, EditarDireccion, ListarDireccion, EliminarDireccion
from .views import logout_user
from .views import ModificarEstadoEnvio, EliminarVenta
from .views import EscribirComentario, EliminarComentario, listarComentarios, EditarComentar
from .views import verificar_existe_seguidor, agregar_nuevo_seguidor
from .views import guardar_token
from .views import aniadir_favoritos
from .views import listarFavoritos
from .views import listarCategoria, listarSubCategoria1
from .views import listarDepartamento, listarMunicipio,listarBCanton

app_name='tienda'
urlpatterns=[
    path('', index.as_view(), name='index'),
    path('perfil_info/<int:pk>',UsuarioDetalle.as_view(), name='infoUsuario'),
    path('perfil_info/editar_cliente/<int:pk>', EditarInformacionPerfilCliente.as_view(), name='editarUsuario'),#pk es el ID del perfil
    path('perfil_info/editar_provee/<int:pk>', EditarInformacionPerfilProveedor.as_view(), name="editarProveedor"),
    path('seguidores/verifica_seguidor/<int:pk>', verificar_existe_seguidor, name='verifica_seguidor'),# pk es id del proveedor #}
    path('seguidores/nuevo_seguidor/<int:pk>',agregar_nuevo_seguidor, name="nuevo_seguidor"),
    path('registrar', register, name='registrar'),
    path('registrar/perfil_clien', RegistrarPerfilCliente, name='perfil_cli'),
    path('registrar/perfil_provee',RegistrarPerfilProveedor, name='reg_provee'),
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
    path('producto/detalle_producto/<slug:url>/<int:pk>', DetalleProducto.as_view(), name='detalle_prod'),#muestra informacion de un producto especifico pk es el id de un producto especifico
    path('producto/comentario', EscribirComentario, name='w_coment'),
    path('producto/comentario/listarComent/<int:pk>',listarComentarios, name='ListarComment' ),
    path('producto/comentario/<int:pk>', EliminarComentario, name='del_coment'),
    path('producto/comentario/editar_coment', EditarComentar, name='editar_coment'),
    path('producto/buscar_tienda', buscar_producto_tienda, name='prod_search'),#para buscar ten la tienda del proveedor
    path('producto/cargar_todos_prod', cargar_todos_productos_tienda, name='prod_all'),
    path('venta/eliminar_venta/<int:pk>', EliminarVenta.as_view(), name='del_venta'),#Elimina la venta reaizada por un cliente sirve para que no se llene de ventas el proveedor
    path('venta/registrar_venta/<int:pk>', RegistrarVenta.as_view(), name='reg_venta'),# pk es el pk del producto el id del usuario se obtiene por medio de la variable request
    path('venta/modi_envio/<int:pk>',ModificarEstadoEnvio.as_view(), name='mod_estado'),#pk seria el id de la cesta que se requiere modificar el estado de envio
    path('venta', ListarVenta.as_view(), name='list_venta'),#el id del cliente de la venta se proporciona por medio del request en la vista 
    path('cesta', ListarCesta.as_view(), name='list_cesta'),#el id del cliente se obtiende por medio del request.user
    path('cesta/agregar_cesta/<int:pk>',Agregar_a_Cesta.as_view(), name='agregar_cesta'),#el id del usuario se proporciona por el request variable pk es el id del producto asociado
    path('cesta/actualizar_cesta/<int:pk>', ActualizarCesta.as_view(), name='actualizar_cesta'),#pk recive el id de la cesta a editar
    path('cesta/eliminar_cesta/<int:pk>', EliminarCesta.as_view(), name='eliminar_cesta'),#pk es el id del articulo a eliminar
    path('sub_categoria/<int:pk>', ListarSubCategoria.as_view(), name='sub_categoria'), #pk seria el valor de la Categia padre
    path('guardar-token/', guardar_token, name='guardar_token'),
    path('aniadir_favoritos/<int:pk>', aniadir_favoritos, name='favorito'),#pk es el id de un producto especifico que el cliente agrega a favorito
    path('favoritos/', listarFavoritos.as_view(), name='list_favoritos'), #pk es el id de un usuario especifico
    path('list_cate/',listarCategoria, name='categorias'),
    path('list_cate/lis_sub_cate1/<int:pk>',listarSubCategoria1, name='subcate1'),
    path('depto/<int:pk>', listarDepartamento, name='depto'),
    path('depto/muni/<int:pk>', listarMunicipio, name='muni'),
    path('depto/muni/barcant/<int:pk>', listarBCanton, name='baBcan'),
]
