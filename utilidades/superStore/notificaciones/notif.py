from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from superStore.views import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json

@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)
        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={'message':'formato de datos no validos'})
        
        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head':data['head'], 'body':data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)
        return JsonResponse(status=200, data={'message':'Web push enviado'})
    except TypeError:
        return JsonResponse(estatus=500, data={'message':'ha ocurrido un error 404'})
