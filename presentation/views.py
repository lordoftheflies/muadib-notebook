import uuid

from django.http import JsonResponse


def live(request):
    # threadw = sio.start_background_task(background_thread)
    return JsonResponse({
        'channel': uuid.uuid4()
    })

