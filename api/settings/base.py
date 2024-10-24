import os
from datetime import timedelta
from pathlib import Path
from decouple import AutoConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
config = AutoConfig()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'rest_framework',
    'drf_standardized_errors',
    'knox',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',    
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'dj_rest_auth.registration',

    # local apps
    'api.apps.base',
    'api.apps.accounts',

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )


# django sites
SITE_ID = 1

# custom user model
AUTH_USER_MODEL = "accounts.User"

# email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="thewkndproject@gmail.com")
SUPPORT_EMAIL = config("SUPPORT_EMAIL", default="thewkndproject@gmail.com")


# rest framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "knox.auth.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 30,
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}

# drf-standardized-errors
DRF_STANDARDIZED_ERRORS = {
    "EXCEPTION_HANDLER_CLASS": "api.exception_handler.CustomExceptionHandler",
}

# django cors headers
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=True, cast=bool)

# allauth config
ACCOUNT_ADAPTER = "api.apps.accounts.adapters.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""


# dj-rest-auth
REST_AUTH = {
    # "USER_DETAILS_SERIALIZER": "api.apps.accounts.serializers.UserSerializer",
    "PASSWORD_RESET_SERIALIZER": "api.apps.accounts.serializers.PasswordResetSerializer",
    "PASSWORD_RESET_CONFIRM_SERIALIZER": "api.apps.accounts.serializers.PasswordResetConfirmSerializer",
    "TOKEN_SERIALIZER": "api.apps.accounts.serializers.TokenSerializer",
    'TOKEN_MODEL': 'knox.models.AuthToken',
    "SESSION_LOGIN": False,
}

# django rest knox
REST_KNOX = {
    "TOKEN_TTL": timedelta(hours=2),
    # "USER_SERIALIZER": "api.apps.accounts.serializers.UserSerializer",
    "AUTH_HEADER_PREFIX": "Bearer",
}

# frontend
FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:3000")
FRONTEND_EMAIL_VERIFICATION_URL = config(
    "FRONTEND_EMAIL_VERIFICATION_URL", default="verify-email/"
)
FRONTEND_RESET_PASSWORD_URL = config(
    "FRONTEND_RESET_PASSWORD_URL", default="reset-password/"
)
FRONTEND_INVITE_URL = config(
    "FRONTEND_INVITE_URL", default="invite/"
)
