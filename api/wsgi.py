"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
from typing import Optional
import os

from django.core.wsgi import get_wsgi_application

settings_module: Optional[str] = os.environ.get("DJANGO_SETTINGS_MODULE")
if not settings_module:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.dev')

application = get_wsgi_application()
