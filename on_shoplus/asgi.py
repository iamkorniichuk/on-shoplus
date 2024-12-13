import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "on_shoplus.settings")

application = get_asgi_application()
