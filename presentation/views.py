import uuid

import socketio
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
mgr = socketio.KombuManager('amqp://')
sio = socketio.Server(
    async_mode=settings.SOCKETIO_ASYNC_MODE,
    client_manager=mgr
)

def live(request):
    # threadw = sio.start_background_task(background_thread)
    return JsonResponse({
        'channel': uuid.uuid4()
    })

@sio.on('live', namespace='/live')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('connect', namespace='/live')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/live')
def message(sid, data):
    print("message ", data)
    sio.emit('reply', room=sid)

@sio.on('disconnect', namespace='/live')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('connect', namespace='/state')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/state')
def message(sid, data):
    print("message ", data)
    sio.emit('reply', room=sid)

@sio.on('disconnect', namespace='/state')
def disconnect(sid):
    print('disconnect ', sid)

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        print('.................................................................................')
        sio.emit('state', {'data': 'Server generated event'})