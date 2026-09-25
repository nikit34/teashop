from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import GuestEmail
from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart, CartItem
from orders.models import Order
from products.models import Product


@override_settings(STRIPE_SECRET_KEY='sk_test_placeholder')
class ReservationCheckoutTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(title='Cabaz Teste - Test Hamper', price=30, quantity=5, delivery=True)
        self.cart = Cart.objects.create()
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        self.cart.save()
        guest = GuestEmail.objects.create(email='buyer@example.com')
        session = self.client.session
        session['cart_id'] = self.cart.id
        session['guest_email_id'] = guest.id
        session.save()
        self.billing_profile = BillingProfile.objects.create(email='buyer@example.com')
        address = Address.objects.create(
            billing_profile=self.billing_profile,
            name='Buyer',
            address_line_1='Rua Augusta 1',
            postal_code='1100-048',
            city='Lisboa',
        )
        self.order = Order.objects.create(billing_profile=self.billing_profile, cart=self.cart, address=address)
        self.order.update_total()

    @patch('billing.models.stripe.Customer.create')
    def test_billing_profile_skips_stripe_without_real_key(self, mock_create):
        profile = BillingProfile.objects.create(email='other@example.com')
        mock_create.assert_not_called()
        self.assertIsNone(profile.customer_id)

    def test_reserve_marks_order_reserved_and_empties_cart(self):
        response = self.client.post(reverse('cart:checkout'), {
            'action': 'reserve',
            'phone': '+351 910 000 000',
            'note': 'Gift for a colleague',
        })
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'reserved')
        self.assertEqual(self.order.phone, '+351 910 000 000')
        self.assertEqual(self.order.note, 'Gift for a colleague')
        self.assertRedirects(
            response,
            reverse('cart:success', kwargs={'orderID': self.order.order_id}),
            fetch_redirect_response=False,
        )
        self.assertNotIn('cart_id', self.client.session)

    def test_reserve_without_phone_keeps_order_open(self):
        self.client.post(reverse('cart:checkout'), {'action': 'reserve', 'phone': '12'})
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'created')

    @patch('billing.models.BillingProfile.charge')
    def test_card_charge_skipped_without_real_stripe_key(self, mock_charge):
        self.client.post(reverse('cart:checkout'))
        mock_charge.assert_not_called()

    def test_checkout_address_accepts_any_portuguese_city(self):
        address = Address.objects.create(
            billing_profile=self.billing_profile,
            name='Buyer',
            address_line_1='Rua do Castelo 5',
            postal_code='8000-000',
            city='Faro',
        )
        address.full_clean()
        self.assertIn('8000-000 Faro', address.get_address())
