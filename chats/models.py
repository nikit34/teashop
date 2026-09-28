from django.db import models
from django.utils.translation import gettext_lazy

from accounts.models import User
from products.models import Product


class Comment(models.Model):
    listing = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', null=True)
    msg = models.TextField(null=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    send_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['send_time']

    def __str__(self):
        return 'Comment {} by {}'.format(self.msg, self.sender)


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    source = models.CharField(max_length=40, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '{} <{}>'.format(self.full_name, self.email)


class WaitlistSignup(models.Model):
    OCCASIONS = [
        ('family', gettext_lazy('Family or friends')),
        ('company', gettext_lazy('My company: team or clients')),
        ('self', gettext_lazy('For myself')),
        ('other', gettext_lazy('Something else')),
    ]

    email = models.EmailField()
    name = models.CharField(max_length=120, blank=True, default='')
    occasion = models.CharField(max_length=20, choices=OCCASIONS, blank=True, default='')
    company = models.CharField(max_length=120, blank=True, default='')
    boxes = models.PositiveIntegerField(null=True, blank=True)
    items = models.TextField(blank=True, default='')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    source = models.CharField(max_length=40, blank=True, default='')
    language = models.CharField(max_length=8, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.email


class DoorHit(models.Model):
    cart = models.OneToOneField('carts.Cart', on_delete=models.CASCADE, related_name='door_hit')
    items = models.TextField(blank=True, default='')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    source = models.CharField(max_length=40, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '{} {}'.format(self.timestamp, self.items)
