from django.contrib import admin
from .models import tbl_mayorista, tbl_cliente, tbl_pais, tbl_tipo_usuario, User, tbl_direccion, tbl_categoria, tbl_producto, tbl_venta

# Register your models here.
admin.site.register(User)
admin.site.register(tbl_mayorista)
admin.site.register(tbl_cliente)
admin.site.register(tbl_pais)
admin.site.register(tbl_tipo_usuario)
admin.site.register(tbl_direccion)
admin.site.register(tbl_categoria)
admin.site.register(tbl_producto)
admin.site.register(tbl_venta)