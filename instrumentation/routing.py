from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/live/(?P<room_name>[^/]+)/$', consumers.TerminalConsumer),
    url(r'^terminal/(?P<resource_name>[^/]+)/$', consumers.TerminalConsumer),
]