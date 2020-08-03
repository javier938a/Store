from django.views.generic import ListView
from superStore.models import tbl_categoria, tbl_sub_categoria1, tbl_sub_categoria2
from superStore.forms import CategoriaForm
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

#lista las categorias principales
def listarCategoria(request):
    categoria=None
    if request.is_ajax():
        categoria = tbl_categoria.objects.all()
    
    return JsonResponse(serialize('json', categoria), safe=False)
#lista las categorias de nivel 1
def listarSubCategoria1(request, pk):#pk es ek id  de la categoria
    print("llego...")
    sub_categoria1 = None
    if request.is_ajax():
        sub_categoria1 = tbl_sub_categoria1.objects.filter(categoria__id = pk)

    return JsonResponse(serialize('json',sub_categoria1), safe=False)

def listarSubCategoria2(request, pk):
    sub_categoria2 = None
    print("esta aqui....")
    if request.is_ajax():
        sub_categoria2 = tbl_sub_categoria2.objects.filter(categoria__id=pk)
    
    return JsonResponse(serialize('json', sub_categoria2), safe=False)
