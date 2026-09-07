import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-gso-2025-key-change-in-production!')
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'observer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'globalsouthobserver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'observer.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'globalsouthobserver.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # IST — UTC+05:30
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── NewsAPI ───────────────────────────────────────────────────────────────────
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '16028ee041dd4f37ba9c619ea1ee9a08')
NEWS_API_BASE_URL = 'https://newsapi.org/v2/'

# ── Site Info ─────────────────────────────────────────────────────────────────
SITE_NAME = 'The Global South Observer'
SITE_TAGLINE = 'Voice of Global South'

SOCIAL_LINKS = {
    'email': 'contactglobalsouthobserver@gmail.com',
    'facebook': 'https://www.facebook.com/',
    'youtube': 'https://www.youtube.com/@GlobalSouthObserver-z4y',
    'linkedin': 'https://www.linkedin.com/groups/40128007/',
    'instagram': 'https://www.instagram.com/globalsouthobserver/',
    'twitter': 'https://x.com/globalsouthobsr',
    'whatsapp': 'https://chat.whatsapp.com/C6cLmw72c8KI2cx3gUOkaT',
}

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG:   'debug',
    messages.INFO:    'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR:   'error',
}

# ── Auth redirects ────────────────────────────────────────────────────────────
LOGIN_URL          = '/author/login/'
LOGIN_REDIRECT_URL = '/author/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ── File upload size limit (10 MB) ────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
