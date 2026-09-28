from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from carts.models import Cart
from chats.models import DoorHit, WaitlistSignup
from products.models import Product


@override_settings(PRELAUNCH=True)
class PrelaunchTests(TestCase):
    def setUp(self):
        self.box = Product.objects.create(title='Cabaz Teste - Test Hamper', price=26, quantity=15)

    def test_every_page_says_we_are_not_selling(self):
        response = self.client.get('/en/')
        self.assertContains(response, 'we are not selling yet')
        detail = self.client.get(self.box.get_absolute_url())
        self.assertContains(detail, 'not for sale yet')
        self.assertNotContains(detail, 'Pay after confirmation')

    def test_checkout_leads_to_the_waitlist(self):
        self.client.post(reverse('cart:update'), {'product_id': self.box.id, 'new_quantity': 1})
        response = self.client.get(reverse('cart:checkout'))
        self.assertRedirects(response, reverse('waitlist'), fetch_redirect_response=False)
        cart_page = self.client.get(reverse('cart:home'))
        self.assertContains(cart_page, reverse('waitlist'))
        self.assertNotContains(cart_page, 'href="{}"'.format(reverse('cart:checkout')))

    def test_signup_keeps_the_picked_items_and_the_link_source(self):
        self.client.get('/en/?src=tg-peopleofporto')
        self.client.post(reverse('cart:update'), {'product_id': self.box.id, 'new_quantity': 2})
        response = self.client.post(reverse('waitlist'), {
            'email': 'ana@example.pt',
            'occasion': 'company',
            'company': 'Atelier Teste',
            'boxes': 12,
        })
        self.assertRedirects(response, reverse('waitlist-thanks'), fetch_redirect_response=False)
        signup = WaitlistSignup.objects.get()
        self.assertEqual(signup.items, '2 x Cabaz Teste')
        self.assertEqual(signup.source, 'tg-peopleofporto')
        self.assertEqual((signup.company, signup.boxes), ('Atelier Teste', 12))
        self.assertEqual(signup.total, 52)
        out = StringIO()
        call_command('reservations', stdout=out)
        self.assertIn('Waitlist signups: 1', out.getvalue())

    def test_signup_needs_an_email(self):
        response = self.client.post(reverse('waitlist'), {'occasion': 'family'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(WaitlistSignup.objects.exists())

    def test_terms_say_there_is_no_sale_yet(self):
        self.assertContains(self.client.get('/en/terms/'), 'does not sell or deliver yet')
        self.assertContains(self.client.get('/pt/terms/'), 'ainda não vende nem entrega')
        self.assertContains(self.client.get('/en/privacy/'), 'Pre-launch list')


class SalesModeTests(TestCase):
    def test_checkout_is_the_normal_one_when_not_in_prelaunch(self):
        response = self.client.get('/en/')
        self.assertNotContains(response, 'prelaunch-banner')


@override_settings(FAKE_DOOR=True)
class FakeDoorTests(TestCase):
    def setUp(self):
        self.box = Product.objects.create(title='Cabaz Teste - Test Hamper', price=26, quantity=15)

    def test_shop_looks_open_but_makes_no_service_promises(self):
        home = self.client.get('/en/')
        self.assertNotContains(home, 'prelaunch-banner')
        self.assertNotContains(home, 'Pay after we confirm your order')
        detail = self.client.get(self.box.get_absolute_url())
        self.assertNotContains(detail, 'Pay after confirmation')
        self.assertNotContains(detail, 'we confirm availability within 24 hours')
        self.assertNotContains(detail, 'not for sale yet')

    def test_checkout_click_is_counted_once_and_then_disclosed(self):
        self.client.get('/en/?src=tg-portugaliada')
        self.client.post(reverse('cart:update'), {'product_id': self.box.id, 'new_quantity': 1})
        cart_page = self.client.get(reverse('cart:home'))
        self.assertContains(cart_page, 'href="{}"'.format(reverse('cart:checkout')))
        response = self.client.get(reverse('cart:checkout'))
        self.assertRedirects(response, reverse('waitlist'), fetch_redirect_response=False)
        self.client.get(reverse('cart:checkout'))
        hit = DoorHit.objects.get()
        self.assertEqual((hit.items, hit.source, hit.total), ('1 x Cabaz Teste', 'tg-portugaliada', 26))
        self.assertContains(self.client.get(reverse('waitlist')), 'We are not selling yet')
        out = StringIO()
        call_command('reservations', stdout=out)
        self.assertIn('Checkout clicks (fake door): 1', out.getvalue())

    def test_empty_cart_click_is_not_counted(self):
        self.client.get(reverse('cart:checkout'))
        self.assertFalse(DoorHit.objects.exists())

    def test_terms_still_say_there_is_no_sale(self):
        self.assertContains(self.client.get('/en/terms/'), 'does not sell or deliver yet')
