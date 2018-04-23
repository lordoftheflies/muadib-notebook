import logging
import os
import socketio
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muadib.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')

import configurations


configurations.setup()

logger = logging.getLogger(__name__)

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
basedir = settings.BASE_DIR
mgr = socketio.KombuManager('amqp://')
sio = socketio.Server(async_mode=settings.SOCKETIO_ASYNC_MODE, client_manager=mgr)
thread = None
from muadib.wsgi import application
# wrap WSGI application with socketio's middleware
app = socketio.Middleware(socketio_app=sio, wsgi_app=application, socketio_path='live')
logger.warning('socket-io service initialized')