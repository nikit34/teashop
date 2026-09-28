from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from carts.models import Cart
from products.models import Product


class SourceTagTests(TestCase):
    def test_link_tag_is_kept_on_the_cart(self):
        self.client.get('/en/?src=fb-expats-lisboa')
        cart = Cart.objects.get(id=self.client.session['cart_id'])
        self.assertEqual(cart.source, 'fb-expats-lisboa')

    def test_first_tag_of_a_cart_stays(self):
        self.client.get('/en/?src=email-b2b')
        self.client.get('/en/?src=fb-expats-porto')
        cart = Cart.objects.get(id=self.client.session['cart_id'])
        self.assertEqual(cart.source, 'email-b2b')
        self.assertEqual(self.client.session['src'], 'fb-expats-porto')

    def test_unsafe_tag_is_ignored(self):
        self.client.get('/en/?src=%3Cscript%3E')
        self.assertNotIn('src', self.client.session)

    def test_report_counts_by_source(self):
        self.client.get('/en/?src=fb-expats-lisboa')
        out = StringIO()
        call_command('reservations', stdout=out)
        self.assertIn('By source', out.getvalue())
        self.assertIn('fb-expats-lisboa', out.getvalue())


class MinimumQuantityTests(TestCase):
    def test_corporate_box_goes_into_the_cart_as_ten(self):
        box = Product.objects.create(title='Cabaz Empresas Teste - Corporate Box', price=45, quantity=100, min_quantity=10)
        self.client.post(reverse('cart:update'), {'product_id': box.id, 'new_quantity': 1})
        cart = Cart.objects.get(id=self.client.session['cart_id'])
        self.assertEqual(cart.cart_items.get(product=box).quantity, 10)


@override_settings(
    SELLER_NAME='Nome Teste',
    SELLER_NIF='123456789',
    SELLER_ADDRESS='Rua Augusta 1, 1100-048 Lisboa',
    SELLER_EMAIL='ola@example.pt',
)
class LegalInformationTests(TestCase):
    def test_footer_shows_seller_and_complaints_book(self):
        response = self.client.get('/pt/')
        self.assertContains(response, 'Nome Teste')
        self.assertContains(response, 'NIF 123456789')
        self.assertContains(response, 'livroreclamacoes.pt')
        self.assertContains(response, 'cniacc.pt')

    def test_terms_and_privacy_in_both_languages(self):
        pages = (
            ('/pt/terms/', 'Termos e condições'),
            ('/en/terms/', 'Terms and conditions'),
            ('/pt/privacy/', 'Política de privacidade'),
            ('/en/privacy/', 'Privacy policy'),
        )
        for url, heading in pages:
            response = self.client.get(url)
            self.assertContains(response, heading)
            self.assertContains(response, 'Nome Teste')

    def test_no_third_party_tracking_on_public_pages(self):
        response = self.client.get('/en/')
        self.assertNotContains(response, 'googletagmanager')
        self.assertNotContains(response, 'paypal.com/sdk')
        self.assertNotContains(response, 'tinyInject')
