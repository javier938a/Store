from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
import json

from fcm_django.models import FCMDevice

@csrf_exempt
@require_http_methods(['POST',])
def guardar_token(request):
    print("Helowwww")
    body = request.body.decode('utf-8')
    print(body)
    bodyDic=json.loads(body)

    token = bodyDic['token']

    existe = FCMDevice.objects.filter(registration_id=token, active =True)
    if(len(existe)>0):
        return HttpResponseBadRequest(json.dumps({'mensaje':'el token ya existe'}))
    print("Helowwww")
    dispositivo = FCMDevice()
    dispositivo.registration_id = token
    dispositivo.active = True
    #solo si el usuario esta enlazadfo lo vamos a guardar
    if request.user.is_authenticated:
        dispositivo.user = request.user
    
    try:
        dispositivo.save()
        return json.dumps({'mensaje':'token guardado'})
    except:
        return HttpResponseBadRequest(json.dumps({'mensaje':'No se ha podido guardar'}))