from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from accounts.models import User
from analytics.views import SalesAjaxView, SalesView


class SalesAjaxViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        self.staff_user = User.objects.create(
            email='staffmodeltest@gmail.com',
            full_name='Staff Test',
            password='stafftest',
            staff=True
        )

    def test_get_sales_data(self):
        request = self.factory.get('analytics/sales/data/')
        request.user = self.user

        mutable_get = request.GET.copy()
        mutable_get['type'] = 'week'
        request.GET = mutable_get

        response = SalesAjaxView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_sales_data_4weeks(self):
        request = self.factory.get('analytics/sales/data/')
        request.user = self.staff_user
        request.GET = request.GET.copy()
        request.GET['type'] = '4weeks'

        response = SalesAjaxView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class SalesViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def test_sales_view(self):
        request = self.factory.get('analytics/sales/')
        request.user = self.user

        response = SalesView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_sales_view_unauthorized(self):
        request = self.factory.get('analytics/sales/')
        request.user = AnonymousUser()

        response = SalesView.as_view()(request)

        self.assertEqual(response.status_code, 200)
