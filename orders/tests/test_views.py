from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from accounts.forms import User
from billing.models import BillingProfile
from carts.models import Cart
from orders.models import Order, ProductPurchase
from orders.views import VerifyOwnership
from products.models import Product
import json


class OrderListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        self.client.login(username='usermodeltest@gmail.com', password='test')

    def test_order_list_view(self):
        response = self.client.get(reverse('orders:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')


class OrderDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

        cart = Cart.objects.create(user=self.user)

        self.factory = RequestFactory()
        self.request = self.factory.get('orders/list')
        self.request.user = self.user
        self.request.session = {}
        self.billing_profile, _ = BillingProfile.objects.new_or_get(
            request=self.request
        )
        self.client = Client()
        self.client.login(username='usermodeltest@gmail.com', password='test')
        self.order = Order.objects.create(billing_profile=self.billing_profile, cart=cart)

    def test_order_detail_view(self):
        response = self.client.get(reverse('orders:detail', kwargs={'order_id': self.order.order_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')


class CollectionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def test_collection_view(self):
        response = self.client.get(reverse('collection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/collection.html')


class VerifyOwnershipViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        self.factory = RequestFactory()

    def test_verify_ownership_view_owner_true(self):
        product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99,
            featured=True,
            active=True
        )
        self.request = self.factory.get(
            reverse('orders:verify-ownership'),
            {'product_id': product.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.request.user = self.user
        self.request.session = {}
        billing_profile, _ = BillingProfile.objects.new_or_get(
            request=self.request
        )
        ProductPurchase.objects.create(
            order_id='123',
            billing_profile=billing_profile,
            product=product
        )
        response = VerifyOwnership.as_view()(self.request)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertTrue(response_json['owner'])

    def test_verify_ownership_view_owner_false(self):
        self.request = self.factory.get(
            reverse('orders:verify-ownership'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.request.user = self.user
        self.request.session = {}
        response = VerifyOwnership.as_view()(self.request)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertFalse(response_json['owner'])

    def test_verify_ownership_view_error(self):
        response = self.client.get(reverse('orders:verify-ownership'))
        self.assertEqual(response.status_code, 404)