from unittest.mock import MagicMock

from django.test import TestCase

from carts.models import Cart
from .models import Order, BillingProfile


class OrderManagerQuerySetTests(TestCase):
    def setUp(self):
        cart = Cart.objects.create()
        self.order1 = Order.objects.create(cart=cart, status='paid')
        self.order2 = Order.objects.create(cart=cart, status='shipped')
        self.order3 = Order.objects.create(cart=cart, status='refunded')
        self.order4 = Order.objects.create(cart=cart, status='created')
        self.billing_profile = BillingProfile.objects.create(
            email='billingprofilemodeltest@gmail.com'
        )

    def test_recent(self):
        recent_orders = Order.objects.get_queryset().recent()
        self.assertEqual(list(recent_orders), [self.order4, self.order3, self.order2, self.order1])

    def test_get_sales_breakdown(self):
        breakdown = Order.objects.get_queryset().get_sales_breakdown()
        self.assertIn(self.order1, breakdown['recent'])
        self.assertIn(self.order2, breakdown['recent'])
        self.assertNotIn(self.order3, breakdown['recent'])
        self.assertIn(self.order4, breakdown['recent'])
        self.assertNotIn(self.order1, breakdown['shipped'])
        self.assertIn(self.order2, breakdown['shipped'])
        self.assertNotIn(self.order3, breakdown['shipped'])
        self.assertNotIn(self.order4, breakdown['shipped'])
        self.assertIn(self.order1, breakdown['paid'])
        self.assertNotIn(self.order2, breakdown['paid'])
        self.assertNotIn(self.order3, breakdown['paid'])
        self.assertNotIn(self.order4, breakdown['paid'])



