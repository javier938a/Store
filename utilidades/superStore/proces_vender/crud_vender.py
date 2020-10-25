from django.http import request
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.core.serializers import serialize
from superStore.models import tbl_producto
from django.db.models import Q

class OpVender(TemplateView):
    template_name='superStore/proces_vender/op_vender.html'


def listar_productos(request):
    productos=None
    if request.is_ajax():
        productos = tbl_producto.objects.filter(Q(mayorista__user__id=request.user.id))
        print(productos)
    return JsonResponse(serialize('json', productos), safe=False)