from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from products.models import BundleItem, Product


class BundleTests(TestCase):
    def setUp(self):
        self.oil = Product.objects.create(title='Azeite Teste - Test Oil', price=Decimal('12.90'), quantity=5)
        self.honey = Product.objects.create(title='Mel Teste - Test Honey', price=Decimal('9.90'), quantity=5)
        self.hamper = Product.objects.create(title='Cabaz Teste - Test Hamper', price=Decimal('20.00'), quantity=5)
        BundleItem.objects.create(bundle=self.hamper, item=self.oil, quantity=1)
        BundleItem.objects.create(bundle=self.hamper, item=self.honey, quantity=2)

    def test_bundle_value_and_saving(self):
        self.assertEqual(self.hamper.bundle_value, Decimal('32.70'))
        self.assertEqual(self.hamper.bundle_saving, Decimal('12.70'))
        self.assertTrue(self.hamper.is_bundle)
        self.assertFalse(self.oil.is_bundle)
        self.assertEqual(self.oil.bundle_saving, Decimal('0'))

    def test_no_saving_when_items_cost_less_than_hamper(self):
        self.hamper.price = Decimal('40.00')
        self.assertEqual(self.hamper.bundle_saving, Decimal('0'))

    def test_detail_lists_contents_and_saving(self):
        response = self.client.get(self.hamper.get_absolute_url())
        self.assertContains(response, 'Mel Teste')
        self.assertContains(response, '2 &times;')
        self.assertContains(response, '12.70')

    def test_credits_page_lists_only_sourced_photos(self):
        self.oil.image_credit = 'Jane Doe / Flickr, CC BY 2.0'
        self.oil.image_source_url = 'https://www.flickr.com/photos/jane/1'
        self.oil.save()
        response = self.client.get(reverse('credits'))
        self.assertContains(response, 'Jane Doe / Flickr, CC BY 2.0')
        self.assertNotContains(response, 'Cabaz Teste')
