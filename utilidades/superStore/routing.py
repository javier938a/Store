from django.urls import re_path
from .consumers import NotificacionConsumer

websocket_urlpatterns = [
    re_path(r'ws/notificacion/(?P<room_name>\w+)/$', NotificacionConsumer),
]