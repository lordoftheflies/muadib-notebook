from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import instrumentation.routing

application = ProtocolTypeRouter(dict(websocket=AuthMiddlewareStack(
    URLRouter(instrumentation.routing.websocket_urlpatterns)
)))
