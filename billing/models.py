import stripe
from django.conf import settings
from django.contrib import messages
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext

from accounts.models import GuestEmail

STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', None)
stripe.api_key = STRIPE_SECRET_KEY

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None

        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, payment_type, order_obj, *args):
        if payment_type == 'S':
            return Charge.objects.do(self, order_obj)
        elif payment_type == 'P':
            return PaypalCharge.objects.do(self, order_obj, args[0])
        else:
            raise KeyError("Invalid type payment")

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing-payment-method')

    @property
    def has_card(self):
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(email=instance.email)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'token': token,
                },
            )
            stripe.PaymentMethod.attach(
                payment_method.id,
                customer=customer.id,
            )
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_id=payment_method.id,
                brand=payment_method.card.brand,
                country=payment_method.card.country,
                exp_month=payment_method.card.exp_month,
                exp_year=payment_method.card.exp_year,
                last4=payment_method.card.last4
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
    stripe_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return '{} {}'.format(self.brand, self.last4)


def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created or instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)


post_save.connect(new_card_post_save_receiver, sender=Card)


class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, gettext('No cards available')
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(float(order_obj.total) * 100),
                currency='usd',
                customer=billing_profile.customer_id,
                payment_method=card_obj.stripe_id,
                confirm=True,
                metadata={'order_id': order_obj.order_id},
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never'
                },
            )
            new_charge_obj = self.model(
                billing_profile=billing_profile,
                stripe_id=intent.id,
                status=intent.status
            )
            new_charge_obj.save()
            return new_charge_obj.status, new_charge_obj.stripe_id

        except stripe.error.CardError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('cart:home')
        except stripe.error.InvalidRequestError as e:
            messages.success(self.request, "Invalid request")
            return redirect('cart:home')
        except stripe.error.AuthenticationError as e:
            messages.success(self.request, "Authentication error")
            return redirect('cart:home')
        except stripe.error.APIConnectionError as e:
            messages.success(self.request, "Check your connection")
            return redirect('cart:home')
        except stripe.error.StripeError as e:
            messages.success(
                self.request, "There was an error please try again")
            return redirect('cart:home')
        except Exception as e:
            messages.success(
                self.request, "A serious error occured we were notified")
            return redirect('cart:home')


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
    stripe_id = models.CharField(max_length=120)
    status = models.CharField(max_length=20, null=True, blank=True)

    objects = ChargeManager()


class PaypalChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, paypal_response):
        try:
            new_charge_obj = self.model(
                billing_profile=billing_profile,
                paypal_id=paypal_response.result.id,
                paid=True,
                intent=paypal_response.result.intent,
                status=paypal_response.result.status,
                create_time=paypal_response.result.create_time
            )
            new_charge_obj.save()
            return new_charge_obj.paid, new_charge_obj.paypal_id
        except Exception as e:
            messages.success(
                self.request, "A serious error occured we were notified")
            return redirect('cart:home')


class PaypalCharge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
    paypal_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    intent = models.CharField(max_length=60)
    status = models.CharField(max_length=60)
    create_time = models.DateTimeField()

    objects = PaypalChargeManager()
