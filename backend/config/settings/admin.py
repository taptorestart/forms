from config.settings.base import *

load_dotenv()


ROOT_URLCONF = "config.urls.admin"

INSTALLED_APPS += [
    "unfold",  # Django Admin Theme before django.contrib.admin
    "django.contrib.admin",
]

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"
