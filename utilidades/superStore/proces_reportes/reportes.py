from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core.serializers import serialize

class Reportes(TemplateView):
    template_name='superStore/proces_reportes/reportes.html'

def reporte_diario(request):
    pass