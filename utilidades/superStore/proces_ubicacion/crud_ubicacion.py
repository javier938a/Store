from superStore.models import tbl_pais
from superStore.models import tbl_departamento
from superStore.models import tbl_municipio
from superStore.models import tbl_barrio_canton
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers import serialize

def listarDepartamento(request, pk):
    departamento=None
    if request.is_ajax():
        departamento = tbl_departamento.objects.filter(Q(pais__id=pk))

    return JsonResponse(serialize('json', departamento), safe=False)

def listarMunicipio(request, pk):
    municipio = None
    if request.is_ajax():
        municipio = tbl_municipio.objects.filter(Q(departamento__id=pk))

    return JsonResponse(serialize('json', municipio), safe=False)

def listarBCanton(request, pk):
    barrioCanton = None
    if request.is_ajax():
        barrioCanton = tbl_barrio_canton.objects.filter(Q(municipio__id=pk))
    
    return JsonResponse(serialize('json', barrioCanton), safe=False)

