import os

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application


os.environ['DJANGO_SETTINGS_MODULE'] = 'eCommerce_Django.settings'
application = StaticFilesHandler(get_wsgi_application())
