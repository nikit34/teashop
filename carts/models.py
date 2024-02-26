from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save

from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id')
        user = request.user
        new_obj = False

        if cart_id is not None:
            cart_obj = self.get_queryset().filter(id=cart_id).first()
            if cart_obj:
                if user.is_authenticated and cart_obj.user is None:
                    cart_obj.user = user
                    cart_obj.save()
            else:
                cart_obj = self.new(user=user)
                new_obj = True
                request.session['cart_id'] = cart_obj.id
        else:
            cart_obj = self.new(user=user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id

        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def delivery(self):
        return self.cart_items.filter(product__delivery=True).exists()


def cart_post_save_receiver(sender, instance, created, **kwargs):
    cart = instance.cart
    subtotal = Decimal(0)
    for item in cart.cart_items.all():
        subtotal += item.product.price * item.quantity
    cart.subtotal = subtotal
    cart.save(update_fields=['subtotal'])


post_save.connect(cart_post_save_receiver, sender=CartItem)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal  # here can change final cost
    else:
        instance.total = Decimal(0.00)


pre_save.connect(product_pre_save_receiver, sender=Cart)
