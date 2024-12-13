from pathlib import Path
from environs import Env


env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ROOT_URLCONF = "on_shoplus.urls"
WSGI_APPLICATION = "on_shoplus.wsgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = env.str("STATIC_FOLDER")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
