from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.serializers import serialize
from django.db.models import Q
import json

from fcm_django.models import FCMDevice

@csrf_exempt
@require_http_methods(['POST',])
def guardar_token(request):
    dispositivo=None
    if request.user.is_authenticated:
        print("Helowwww1")
        body = request.body.decode('utf-8')
        print(body)
        bodyDic=json.loads(body)

        token = bodyDic['token']


        existe = FCMDevice.objects.filter(Q(registration_id=token) & Q(active =True))
        if existe.exists():
            user_token = FCMDevice.objects.get(Q(registration_id=token) & Q(active=True))
            if user_token.user==request.user:
                print("el token generado corresponde a: "+str(user_token.user))
                return JsonResponse({
                    'mensaje':'El token ya existe',
                }, safe=False)
            else:
                print("El token existe pero no corresponde al usuario autenticado")
                existe = FCMDevice.objects.filter(Q(user=request.user) & Q(active=True))
                if existe.exists():  
                    #print(existe.registration_id)
                    print("El usuario que no corresponde al token ya esta registrado sin token o con otro token ") 
                    return JsonResponse({
                        'mensaje':'El usuario que no corresponde al token ya esta registrado sin token',
                    }, safe=False)
                else:                 
                    dispositivo = FCMDevice()
                    try:
                        dispositivo.user=request.user
                        dispositivo.active=True
                        dispositivo.save()
                    except:
                        return JsonResponse({
                            'mensaje':'Hubo un error al intentar guardar',
                        }, safe=False)
                    
                return JsonResponse({
                    'mensaje':'El token existe pero no corresponde al usuario autenticado',
                }, safe=False)
        else:
            #verificar hay un usuario registrado sin token
            exit_not_token = FCMDevice.objects.filter(Q(user=request.user) & Q(active=True))
            if exit_not_token.exists():
                update = FCMDevice.objects.filter(Q(user=request.user) & Q(active=True)).update(registration_id=str(token))
                print("Se le ha registrado este token a este usuario que habia sido registrado sin token: "+str(update))
                return JsonResponse({
                    'mensaje':'se le ha registrado este token a este usuario que habia sido registrado sin token',
                }, safe=False)
            else:
                try:
                    dispositivo = FCMDevice()
                    dispositivo.registration_id = str(token)
                    dispositivo.user=request.user
                    dispositivo.active=True
                    #guardando informacion
                    dispositivo.save()
                except:
                    return JsonResponse({
                        'mensaje':'Hubo un error al intentar guardar el token',
                    }, safe=False)

    return JsonResponse({
        'mensaje':'Usuario y token guardados..',
    }, safe=False)