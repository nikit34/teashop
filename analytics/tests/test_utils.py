from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from analytics.utils import get_client_ip
User = get_user_model()


class UtilsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_client_ip_with_x_forwarded_for(self):
        request = self.factory.get('/', HTTP_X_FORWARDED_FOR='192.168.1.1, 192.168.1.2')
        ip = get_client_ip(request)
        self.assertEqual(ip, '192.168.1.1')

    def test_get_client_ip_without_x_forwarded_for(self):
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        ip = get_client_ip(request)
        self.assertEqual(ip, '192.168.1.1')

    def test_get_client_ip_with_no_x_forwarded_for_and_no_remote_addr(self):
        request = self.factory.get('/')
        ip = get_client_ip(request)
        self.assertEqual(ip, '127.0.0.1')
