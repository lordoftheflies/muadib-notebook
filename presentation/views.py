import uuid

import socketio
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
mgr = socketio.KombuManager('amqp://')
sio = socketio.Server(async_mode=settings.SOCKETIO_ASYNC_MODE, client_manager=mgr)

def live(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return JsonResponse({
        'channel': uuid.uuid4()
    })

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my response', {'data': 'Server generated event'},
                 namespace='/test')