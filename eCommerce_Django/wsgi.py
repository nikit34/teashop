import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise


os.environ['DJANGO_SETTINGS_MODULE'] = 'eCommerce_Django.settings'
application = get_wsgi_application()
application = WhiteNoise(application)
