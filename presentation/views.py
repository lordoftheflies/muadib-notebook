import uuid

import socketio
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


def live(request):
    # threadw = sio.start_background_task(background_thread)
    return JsonResponse({
        'channel': uuid.uuid4()
    })

