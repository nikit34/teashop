import os

from django.utils.translation import gettext_lazy

from eCommerce_Django.utils import get_optional_secret, get_secret_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = get_secret_key(BASE_DIR, 'SECRET_KEY')

DEBUG = False

DJANGO_TEST_PROCESSES = 8

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://pantry.carsbuyer.org']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',

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
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'logs', 'mail')
ACCOUNT_EMAIL_VERIFICATION = False
DEFAULT_FROM_EMAIL = SUPPORT_EMAIL
MANAGERS = (
    ('Nikita', SUPPORT_EMAIL),
)
ADMINS = MANAGERS


BASE_URL = 'https://pantry.carsbuyer.org'


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
    'eCommerce_Django.middleware.SourceTagMiddleware',
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
                'eCommerce_Django.context_processors.store',
            ],
        },
    },
]

WSGI_APPLICATION = 'eCommerce_Django.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

LANGUAGES = [('en', 'English'), ('pt', 'Português'), ]

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

STORE_NAME = 'Portuguese Pantry'
STORE_TAGLINE = gettext_lazy('Curated food and gifts from small Portuguese producers')

SELLER_NAME = get_optional_secret(BASE_DIR, 'SELLER_NAME')
SELLER_NIF = get_optional_secret(BASE_DIR, 'SELLER_NIF')
SELLER_ADDRESS = get_optional_secret(BASE_DIR, 'SELLER_ADDRESS')
SELLER_EMAIL = get_optional_secret(BASE_DIR, 'SELLER_EMAIL')
SELLER_PHONE = get_optional_secret(BASE_DIR, 'SELLER_PHONE')
SELLER_VAT_EXEMPT = get_optional_secret(BASE_DIR, 'SELLER_VAT_EXEMPT') == 'yes'
