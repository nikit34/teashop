from unittest.mock import patch

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.http import JsonResponse

from carts.models import Cart, CartItem
from products.models import Product
from carts import views


class CartViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(title='Test Product', price=10.00, quantity=5, delivery=True)

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_cart_detail_api_view(self):
        request = self.factory.get(reverse('apis:api-cart'))
        request.user = AnonymousUser()
        request.session = {}
        response = views.cart_detail_api_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_cart_home(self):
        response = self.client.get(reverse('cart:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carts/home.html')

    def test_cart_update_invalid_product_id(self):
        response = self.client.post(reverse('cart:update'), {'product_id': '100', 'new_quantity': '3'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)

    def test_cart_update_valid_product_id(self):
        request = self.factory.post(reverse('cart:update'), {'product_id': self.product.id, 'new_quantity': '3'})
        request.user = AnonymousUser()
        request.session = {}
        response = views.cart_update(request)
        self.assertEqual(response.status_code, 302)

    def test_checkout_home_redirect_empty_cart(self):
        request = self.factory.get(reverse('cart:checkout'))
        request.user = AnonymousUser()
        request.session = {}
        response = views.checkout_home(request)
        self.assertEqual(response.status_code, 302)

    @patch('billing.models.BillingProfile.charge')
    @patch('billing.models.BillingProfile.has_card', return_value=True)
    def test_checkout_home_successful_order(self, mock_has_card, mock_charge):
        cart = Cart.objects.create()
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.post(reverse('cart:checkout'))
        self.assertEqual(response.status_code, 302)  # Redirects after successful order

    @patch('billing.models.BillingProfile.charge', return_value=('succeeded', 'order_id'))
    def test_checkout_home_failed_charge(self, mock_charge):
        cart = Cart.objects.create()
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.post(reverse('cart:checkout'))
        self.assertEqual(response.status_code, 302)

    def test_checkout_done_view(self):
        order_id = 'test_order_id'
        response = self.client.get(reverse('cart:success', kwargs={'orderID': order_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carts/checkout/done.html')
