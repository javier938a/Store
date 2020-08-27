from django.urls import re_path
from .consumers import NotificacionConsumer, ChatConsumer, NotiConsumer

websocket_urlpatterns = [
    re_path(r'ws/noti/(?P<user>\w+)/$', NotiConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
]