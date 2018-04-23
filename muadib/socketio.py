import os
import socketio
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muadib.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')

import configurations


configurations.setup()

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
basedir = settings.BASE_DIR
sio = socketio.Server(async_mode=settings.SOCKETIO_ASYNC_MODE)
thread = None