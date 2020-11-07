from django.contrib import admin
from .models import tbl_mayorista, tbl_cliente, tbl_pais, tbl_tipo_usuario, User, tbl_direccion, tbl_categoria, tbl_producto, tbl_venta
from .models import tbl_departamento, tbl_municipio, tbl_barrio_canton, tbl_cesta, tbl_sub_categoria1
from .models import tbl_estado_envio, tbl_comentario_producto, tbl_seguidores, tbl_favoritos
from .models import tbl_clients_connect
from .models import tbl_bandeja_de_entrada_cliente, tbl_bandeja_de_salida_cliente, tbl_bandeja_de_entrada_mayorista, tbl_bandeja_de_salida_mayorista
from .models import tbl_factura, tbl_caja, tbl_cajero
from .models import tbl_proveedor
# Register your models here.
admin.site.register(User)
admin.site.register(tbl_mayorista)
admin.site.register(tbl_cliente)
admin.site.register(tbl_pais)
admin.site.register(tbl_departamento)
admin.site.register(tbl_municipio)
admin.site.register(tbl_barrio_canton)
admin.site.register(tbl_tipo_usuario)
admin.site.register(tbl_direccion)
admin.site.register(tbl_categoria)
admin.site.register(tbl_sub_categoria1)
admin.site.register(tbl_producto)
admin.site.register(tbl_venta)
admin.site.register(tbl_cesta)
admin.site.register(tbl_estado_envio)
admin.site.register(tbl_comentario_producto)
admin.site.register(tbl_seguidores)
admin.site.register(tbl_favoritos)
admin.site.register(tbl_clients_connect)
admin.site.register(tbl_bandeja_de_entrada_cliente)
admin.site.register(tbl_bandeja_de_salida_cliente)
admin.site.register(tbl_bandeja_de_entrada_mayorista)
admin.site.register(tbl_bandeja_de_salida_mayorista)
admin.site.register(tbl_factura)
admin.site.register(tbl_cajero)
admin.site.register(tbl_caja)
admin.site.register(tbl_proveedor)