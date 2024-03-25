from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Cart, CartItem
from products.models import Product

User = get_user_model()


class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def setUp(self):
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99
        )

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertIsInstance(cart, Cart)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.subtotal, 0.00)
        self.assertEqual(cart.total, 0.00)

    def test_cart_item_creation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertIsInstance(cart_item, CartItem)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_subtotal_calculation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        cart_item_2 = CartItem.objects.create(cart=cart, product=self.product, quantity=3)
        actual_subtotal = Decimal(self.product.price * (cart_item.quantity + cart_item_2.quantity)).quantize(Decimal('0.00'))
        self.assertEqual(cart.subtotal, actual_subtotal)

    def test_cart_total_calculation(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.total, cart.subtotal)

    def test_cart_delivery_property(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.delivery, True)


class CartSignalsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def setUp(self):
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99
        )

    def test_cart_post_save_receiver(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        cart.refresh_from_db()
        actual_subtotal = Decimal(self.product.price * cart_item.quantity).quantize(Decimal('0.00'))
        self.assertEqual(cart.subtotal, actual_subtotal)
        self.assertEqual(cart.total, cart.subtotal)

    def test_cart_item_post_save_receiver(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        cart.refresh_from_db()
        actual_subtotal = Decimal(self.product.price * cart_item.quantity).quantize(Decimal('0.00'))
        self.assertEqual(cart.subtotal, actual_subtotal)
        self.assertEqual(cart.total, cart.subtotal)

    def test_cart_pre_save_receiver(self):
        cart = Cart.objects.create(user=self.user)
        cart.subtotal = 50.00
        cart.save()
        cart.refresh_from_db()
        self.assertEqual(cart.total, cart.subtotal)
