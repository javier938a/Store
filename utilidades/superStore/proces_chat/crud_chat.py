from superStore.models import tbl_bandeja_de_entrada_cliente, tbl_bandeja_de_salida_cliente
from superStore.models import tbl_bandeja_de_entrada_mayorista, tbl_bandeja_de_salida_mayorista
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q

def get_mensajes_chat(request, grupo):
    bandeja_entrada = None
    chat_cliente=[]
    
    if request.method=="GET":
        mensaje=None
        if request.is_ajax():
            bandeja_salida = tbl_bandeja_de_salida_cliente.objects.filter(grupo=grupo)
            for sms in bandeja_salida:
                bandeja_entrada=tbl_bandeja_de_entrada_cliente.objects.filter(mensaje_salida=sms)
                respuesta=[]#lista donde se almacenaran las respuestas a los mensajes
                for r in bandeja_entrada:#recorriendo las respuestas
                    res={
                        'id':str(r.id),
                        'mayorista':str(r.mayorista),
                        'mensaje':str(r.mensaje),
                        'fecha':str(r.fecha),
                        'grupo':str(r.grupo),
                    }
                    respuesta.append(res)#agregando las respuestas mensaje por mensaje
                    
                mensaje={
                    'id':str(sms.id),
                    'cliente':str(sms.cliente),
                    'mensaje':str(sms.mensaje),
                    'fecha':str(sms.fecha),
                    'grupo':str(sms.grupo),
                    'respuesta':respuesta,
                }
                chat_cliente.append(mensaje)
            
            
                    
            #print(chat_cliente)
                    

    
    return JsonResponse(
        chat_cliente,
        safe=False
    )


                

        
