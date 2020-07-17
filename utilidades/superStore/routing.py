from django.urls import re_path
from .consumers import NotificacionConsumer

websocket_urlpatterns = [
    re_path(r'ws/notificacion/(?P<pk>\w+)/$', NotificacionConsumer),
]