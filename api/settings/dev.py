from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}

# email
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="thewkndproject@gmail.com")
# SUPPORT_EMAIL = config("SUPPORT_EMAIL", default="thewkndproject@gmail.com")