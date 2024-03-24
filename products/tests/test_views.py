from django.test import TestCase
from django.urls import reverse

from products.models import Product


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
