from .base import *  # noqa: F403, F401

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
RATELIMIT_ENABLE = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
MEDIA_ROOT = BASE_DIR / "test_media"  # noqa: F405
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
USE_CLOUDINARY = False
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
MIDDLEWARE = [m for m in MIDDLEWARE if m != "whitenoise.middleware.WhiteNoiseMiddleware"]  # noqa: F405
