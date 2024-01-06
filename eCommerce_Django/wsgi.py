import os
import sys

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

path = os.path.expanduser('/home/TeaShop/teashop.pythonanywhere.com/')
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'eCommerce_Django.settings'

application = StaticFilesHandler(get_wsgi_application())
