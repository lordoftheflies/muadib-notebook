"""
WSGI config for muadib project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
# from socketio import Middleware
import socketio

from presentation.views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muadib.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()

app = socketio.Middleware(socketio_app=sio, wsgi_app=application, socketio_path='live')
