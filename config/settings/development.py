from .base import *  # noqa: F403, F401

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Relaxed security for local dev
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
