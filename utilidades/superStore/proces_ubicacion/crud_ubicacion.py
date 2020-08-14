from superStore.models import tbl_pais
from superStore.models import tbl_departamento
from superStore.models import tbl_municipio
from superStore.models import tbl_barrio_canton
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.generic import ListView

class ListarPais(ListView):#
    template_name='superStore/proces_ubicacion/paises.html'
    context_object_name='paises'
    model = tbl_pais

    def get_context_data(self, **kwargs):
        context = super(ListarPais, self).get_context_data(**kwargs)

        return context
    def get_queryset(self):
        pais_code = self.request.GET.get('pais')
        if pais_code is not None and pais_code is not '':#si pais_code detecta que es None entonces buscaria el pais relacionado a ella
            return self.model.objects.filter(Q(pais__icontains=pais_code))
        return self.model.objects.all()
    

class ListarDepartamentos(ListView):#recivira como parametro el id del pais 
    template_name='superStore/proces_ubicacion/departamentos.html'
    model = tbl_departamento
    context_object_name='depto'

    def get_context_data(self, **kwargs):
        context=super(ListarDepartamentos, self).get_context_data(**kwargs)
        context['id_pais']=self.kwargs['pk']
        return context
    
    def get_queryset(self):
        departamento=self.request.GET.get('depto')
        if departamento is not None:
            return self.model.objects.filter(Q(pais__id=self.kwargs['pk']) & Q(departamento__icontains=departamento))
        
        return self.model.objects.filter(Q(pais__id=self.kwargs['pk']))

class ListarMunicipio(ListView):
    template_name='superStore/proces_ubicacion/municipio.html'
    model=tbl_municipio
    context_object_name='muni'
    def get_context_data(self, **kwargs):
        context = super(ListarMunicipio, self).get_context_data(**kwargs)
        context['id_depto']=self.kwargs['pk']
        return context

    def get_queryset(self):
        municipio = self.request.GET.get('muni')
        if municipio is not None:
            return self.model.objects.filter(Q(departamento__id=self.kwargs['pk']) & Q(municipio__icontains=municipio))
        
        return self.model.objects.filter(Q(departamento__id=self.kwargs['pk']))


class ListarBCanton(ListView):
    template_name='superStore/proces_ubicacion/barrio_canton.html'
    model=tbl_barrio_canton
    context_object_name='bacan'

    def get_context_data(self, **kwargs):
        context=super(ListarBCanton, self).get_context_data(**kwargs)
        context['id_muni']=self.kwargs['pk']
        return context
    
    def get_queryset(self):
        b_c= self.request.GET.get('bacan')
        if b_c is not None:
            return self.model.objects.filter(Q(municipio__id=self.kwargs['pk']) & Q(barrio_canton__icontains=b_c))
        
        return self.model.objects.filter(Q(municipio__id=self.kwargs['pk']))

