from django.test import TestCase, RequestFactory

from accounts.models import User
from carts.models import Cart
from orders.models import Order, BillingProfile


class OrderManagerQuerySetTests(TestCase):
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

        self.order1 = Order.objects.create(billing_profile=self.billing_profile, cart=cart, status='paid')
        self.order2 = Order.objects.create(billing_profile=self.billing_profile, cart=cart, status='shipped')
        self.order3 = Order.objects.create(billing_profile=self.billing_profile, cart=cart, status='refunded')
        self.order4 = Order.objects.create(billing_profile=self.billing_profile, cart=cart, status='created')

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

    def test_by_request(self):
        orders = Order.objects.by_request(self.request)
        self.assertEqual(list(orders), [self.order4, self.order3, self.order2, self.order1])

    def test_not_created(self):
        not_created_orders = Order.objects.get_queryset().not_created()
        self.assertNotIn(self.order4, not_created_orders)
        self.assertIn(self.order1, not_created_orders)
        self.assertIn(self.order2, not_created_orders)
        self.assertIn(self.order3, not_created_orders)
