#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muadib.settings")
    os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')

    import django.core.handlers.wsgi

    application = django.core.handlers.wsgi.WSGIHandler()


    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    PORT = 100
    print('Listening on port %s and on port 843 (flash policy server)' % PORT)