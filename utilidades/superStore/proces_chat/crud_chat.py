from superStore.models import tbl_mensaje_mayorista, tbl_mensaje_cliente, tbl_respuesta_cliente, tbl_respuesta_mayorista 


def listar_mensajes_cliente(request, grupo):
    if request.is_ajax():
        mensajes_cliente = tbl_mensaje_cliente.objects.filter(grupo_privado=grupo)
        for sms in mensajes_cliente:
            respuesta_cliente = tbl_respuesta_cliente.objects.filter(mensaje_cliente__id=mensajes_cliente.id)
            

