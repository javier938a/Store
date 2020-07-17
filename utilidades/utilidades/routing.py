
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import superStore.routing as app

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            app.websocket_urlpatterns
        )
    ),
})