from superStore.models import tbl_compras
from django.views.generic import TemplateView
class Comprar(TemplateView):
    template_name='superStore/proces_compras/comprar_producto.html'