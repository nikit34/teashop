import os

from eCommerce_Django.utils import get_secret_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = get_secret_key(BASE_DIR, 'SECRET_KEY')

DEBUG = False

DJANGO_TEST_PROCESSES = 8

ALLOWED_HOSTS = ['teashop-e3ec3bce7960.herokuapp.com', 'portotea.today']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.postgres',

    'accounts',
    'billing',
    'analytics',
    'addresses',
    'products',
    'carts',
    'marketing',
    'orders',
    'tags',
    'chats',
    'search',
]

SITE_ID = 1

SUPPORT_EMAIL = get_secret_key(BASE_DIR, 'SUPPORT_EMAIL')

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = SUPPORT_EMAIL
EMAIL_HOST_PASSWORD = get_secret_key(BASE_DIR, 'EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SUPPORT_EMAIL
MANAGERS = (
    ('Nikita', SUPPORT_EMAIL),
)
ADMINS = MANAGERS


BASE_URL = 'teashop-e3ec3bce7960.herokuapp.com'


MAILCHIMP_API_KEY = get_secret_key(BASE_DIR, 'MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = 'us10'
MAILCHIMP_EMAIL_LIST_ID = get_secret_key(BASE_DIR, 'MAILCHIMP_EMAIL_LIST_ID')
MAILCHIMP_EMAIL_ADMIN = get_secret_key(BASE_DIR, 'MAILCHIMP_EMAIL_ADMIN')

STRIPE_SECRET_KEY = get_secret_key(BASE_DIR, 'STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = get_secret_key(BASE_DIR, 'STRIPE_PUB_KEY')

PAYPAL_CLIENT_ID = get_secret_key(BASE_DIR, 'PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = get_secret_key(BASE_DIR, 'PAYPAL_CLIENT_SECRET')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]


LOGOUT_REDIRECT_URL = '/login/'
ROOT_URLCONF = 'eCommerce_Django.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'eCommerce_Django.wsgi.application'

HEROKU_DB_PASSWORD = get_secret_key(BASE_DIR, 'HEROKU_DB_PASSWORD')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd3bfl7lu62kgt7',
        'USER': 'u3idpplho8jjur',
        'PASSWORD': HEROKU_DB_PASSWORD,
        'HOST': 'ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

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

SESSION_COOKIE_SAMESITE = 'Lax'

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]

LANGUAGE_CODE = 'en'
# LANGUAGE_CODE = 'ru'

LANGUAGES = [('en', 'English'), ('ru', 'Russian'), ('pt', 'Portugal'), ]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "static_root")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static_cdn", "media_root")

PROTECTED_ROOT = os.path.join(BASE_DIR, "static_cdn", "protected_media")
