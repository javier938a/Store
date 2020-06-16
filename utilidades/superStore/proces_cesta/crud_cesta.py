from django.views.generic import ListView, CreateView, UpdateView
from superStore.models import tbl_cesta, tbl_cliente
from superStore.forms import FormCrearCesta 
from django.urls import reverse_lazy

class ListarCesta(ListView):
    template_name = 'superStore/procesos_cesta/listar_cesta.html'
    context_object_name = 'cesta_list'
    model = tbl_cesta

    def get_queryset(self):
        return self.model.objects.filter(cliente=self.kwargs['pk'])#pk es el cliente al que esta asociada la cesta

class Agregar_a_Cesta(CreateView):
    model = tbl_cesta
    template_name = 'superStore/procesos_cesta/agregar_a_cesta.html'
    context_object_name = 'form'
    form_class = FormCrearCesta
    def get_context_data(self, **kwargs):
        context = super(Agregar_a_Cesta, self).get_context_data()
        context.get('form').fields['cliente'].queryset = tbl_cliente.objects.filter(id=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        precio_unitario = form.cleaned_data['precio_unitario']
        cantidad = form.cleaned_data['cantidad']
        print("esta es la cantidad: "+str(cantidad))
        total = float(precio_unitario)*int(cantidad)
        form.instance.precio_total =total

        form_valid = super(Agregar_a_Cesta,self).form_valid(form)
        print("Sera que guarda? "+str(total))
        return form_valid
        
    def get_success_url(self):
        return reverse_lazy('tienda:list_cesta', args=[str(self.kwargs['pk'])])

class ActualizarCesta(UpdateView):
    model = tbl_cesta
    template_name = 'superStore/procesos_cesta/agregar_a_cesta.html'
    context_object_name = 'form'
    form_class = FormCrearCesta

    def form_valid(self, form):
        precio_unitario = form.cleaned_data['precio_unitario']#obteniendo el precio unitario del formulario
        cantidad = form.cleaned_data['cantidad']
        total = float(precio_unitario)*int(cantidad)
        form.instance.precio_total = total

        form_valid = super(ActualizarCesta, self).form_valid(form)
        return form_valid


    def get_success_url(self):
        return reverse_lazy('tienda:list_cesta', args=[str(self.object.cliente.id)])
