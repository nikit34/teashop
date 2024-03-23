from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductFile


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99,
            featured=True,
            active=True,
            quantity=10
        )

    def test_get_absolute_url(self):
        product = Product.objects.get(title='Test Product')
        self.assertEqual(product.get_absolute_url(), reverse('products:detail', kwargs={'slug': product.slug}))

    def test_product_str_method(self):
        product = Product.objects.get(title='Test Product')
        self.assertEqual(str(product), 'Test Product')
        self.assertEqual(product.slug, "test-product")
        self.assertEqual(product.price, Decimal('10.99') )
        self.assertTrue(product.active)
        self.assertTrue(product.featured)
        self.assertEqual(product.quantity, 10)


class ProductFileModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product",
            price=50.00,
            featured=True,
            active=True,
            quantity=10
        )
        self.product_file = ProductFile.objects.create(
            product=self.product,
            name="Test File",
            description="This is a test file",
        )

    def test_product_file_creation(self):
        product_file = ProductFile.objects.get(name="Test File")
        self.assertEqual(product_file.product, self.product)
        self.assertEqual(product_file.display_name, "Test File")


class ProductViewTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product",
            price=50.00,
            featured=True,
            active=True,
            quantity=10
        )

    def test_product_detail_view(self):
        response = self.client.get(reverse("products:detail", kwargs={"slug": self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
