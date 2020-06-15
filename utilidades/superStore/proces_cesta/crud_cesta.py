from django.views.generic import ListView
from superStore.models import tbl_cesta

class ListarCesta(ListView):
    template_name = 'superStore/procesos_cesta/listar_cesta.html'
    context_object_name = 'cesta_list'
    model = tbl_cesta
    success_url = '/'

    def get_queryset(self):
        return self.model.objects.filter(cliente=self.kwargs['pk'])