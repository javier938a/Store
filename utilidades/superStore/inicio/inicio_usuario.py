from superStore.models import tbl_cliente, User, tbl_cliente, tbl_mayorista
from django.views.generic import DetailView, ListView,TemplateView
from django.shortcuts import render
from superStore.models import tbl_categoria

 
class UsuarioDetalle(DetailView):
    model = User
    template_name = 'superStore/perfil_usuario/perfil.html'
    context_object_name='form'
    def get_context_data(self, **kwargs):
        context = super(UsuarioDetalle, self).get_context_data(**kwargs)
        tipoUsuario = self.kwargs['tipo_usuario']
        perfil = None # creando variable perfil para almacenar perfil
        if tipoUsuario=='Cliente':#Verificando si es Cliente para registrar el perfil del cliente
            perfil_cliente = tbl_cliente.objects.get(user=self.kwargs['pk'])
            context['perfil_cliente']=perfil_cliente
        elif tipoUsuario=='Proveedor':#Verificando si es Proveedor para registrar el perfil del proveedor
            perfil_proveedor = tbl_mayorista.objects.get(user=self.kwargs['pk'])
            context['perfil_proveedor']=perfil_proveedor
         # agregando el perfil al contexto
        print(self.kwargs['pk'])
        return context

def usuario_index(request, pk):
    template = 'superStore/perfil_usuario/index_user.html'
    model_categoria = tbl_categoria.objects.all()
    print(model_categoria)
    model_usuario = User.objects.get(id=pk)# obteniendo todas las categorias existentes
    model_cliente = None#definiendo la variable donde se almacenara un cliente
    model_proveedor = None#definiendo variable donde se almacenara un proveedor
    context = None # deficiendp donde se almacenara el contexto
    ##model_cliente = tbl_cliente.objects.get(user__id=model_usuario.id)
    ##print(model_cliente.user.id)
    if str(model_usuario.tipo_usuario_id) == "Cliente":#si el tipo de usuario es un cliente se creara un modelo cliente en base al ID
        model_cliente = tbl_cliente.objects.get(user__id=model_usuario.id)
        context = {'cate_list':model_categoria, 'cliente':model_cliente}
    elif str(model_usuario.tipo_usuario_id) == "Proveedor":#de lo contrario sera un proveedor
        model_proveedor =tbl_mayorista.objects.get(user__id=model_usuario.id)
        context = {'cate_list':model_categoria, 'proveedor':model_proveedor}
    
    

    return render(request, template,context)

