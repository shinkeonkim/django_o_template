import os
import logging
from pathlib import Path

from django.contrib.messages import constants as messages


# django basic settings
PROJECT_NAME = os.environ.get('PROJECT_NAME')

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG') == 'TRUE'
USE_DOCKER = os.environ.get('USE_DOCKER') == 'TRUE'
PORT = os.environ.get('PORT')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Deploy settings
DEPLOY_URL = os.environ.get('DEPLOY_URL')
ALLOWED_HOSTS = ['*', '127.0.0.1', DEPLOY_URL]

# user model settings
AUTH_USER_MODEL = 'users.User'

ROOT_URLCONF = 'config.urls'

CUSTOM_APPS = [
    'users',
]

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'extra_views',
    'django_unicorn',
    'django_extensions',
    'corsheaders',
    'silk',
    'nplusone.ext.django',
] + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
    'nplusone.ext.django.NPlusOneMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('POSTGRES_NAME'),
        "USER": os.environ.get('POSTGRES_USER'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        "HOST": "db",
        "PORT": os.environ.get('POSTGRES_PORT'),
    }
} if USE_DOCKER else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
    os.path.join(BASE_DIR, 'node_modules'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_HOST_USER = EMAIL_ADDRESS
MAIL_USERNAME = EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = EMAIL_ADDRESS
DEFAULT_FORM_MAIL = os.environ.get('DEFAULT_FORM_MAIL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# sass settings

SASS_PROCESSOR_ENABLED = True
SASS_OUTPUT_STYLE = 'compact'
SASS_PRECISION = 8
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'assets')


# 메세지 프레임워크 클래스 설정

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# debug tool settings
INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# SQL explorer
INSTALLED_APPS += ['explorer']
EXPLORER_CONNECTIONS = {'Default': 'default'}
EXPLORER_DEFAULT_CONNECTION = 'default'

EXPLORER_SQL_BLACKLIST = (
    'ALTER',
    'CREATE TABLE',
    'DELETE',
    'DROP',
    'GRANT',
    'INSERT INTO',
    'OWNER TO'
    'RENAME ',
    'REPLACE',
    'SCHEMA',
    'TRUNCATE',
    'UPDATE',
)

EXPLORER_DEFAULT_ROWS = 1000

EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin'
)

EXPLORER_SCHEMA_INCLUDE_VIEWS = True

# CORS settings
CORS_ALLOWED_ORIGINS = [
    f'http://localhost:{PORT}',
    f'http://127.0.0.1:{PORT}',
]

# N+1 Query auto detector
NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'nplusone': {
            'handlers': ['console'],
            'level': 'WARN',
        },
    },
}
