from decimal import Decimal

from django.test import TestCase
from django.utils import translation

from products.management.commands.seed_gourmet import CATALOG
from products.models import Product


class LocalizedProductTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='Mel de Urze - Heather Honey',
            price=Decimal('9.90'),
            quantity=5,
            description='Dark heather honey from the mountains.',
            description_pt='Mel de urze escuro das serras.',
        )

    def url(self, language):
        with translation.override(language):
            return self.product.get_absolute_url()

    def test_portuguese_page_uses_portuguese_text(self):
        response = self.client.get(self.url('pt'))
        self.assertContains(response, 'Mel de urze escuro das serras.')
        self.assertNotContains(response, 'Dark heather honey')
        self.assertNotContains(response, 'Heather Honey')

    def test_english_page_keeps_english_text(self):
        response = self.client.get(self.url('en'))
        self.assertContains(response, 'Dark heather honey from the mountains.')
        self.assertContains(response, 'Heather Honey')
        self.assertNotContains(response, 'Mel de urze escuro')

    def test_portuguese_falls_back_to_english_description(self):
        self.product.description_pt = ''
        self.product.save()
        self.assertContains(self.client.get(self.url('pt')), 'Dark heather honey from the mountains.')

    def test_every_catalog_item_has_a_portuguese_description(self):
        missing = [spec['title'] for spec in CATALOG if not spec['description_pt'].strip()]
        self.assertEqual(missing, [])
