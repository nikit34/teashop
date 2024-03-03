from django.conf import settings
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressCheckoutForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart

STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', None)
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', None)
stripe.api_key = STRIPE_SECRET_KEY

from .paypal import CreateOrder


def _get_cart_detail(cart_obj):
    products = [{
        'id': item.product.id,
        'url': item.product.get_absolute_url(),
        'title': item.product.title,
        'price': item.product.price,
        'quantity': item.product.quantity,
        'cartItemQuantity': item.quantity
    } for item in cart_obj.cart_items.all()]
    return {
        'products': products,
        'subtotal': cart_obj.subtotal,
        'total': cart_obj.total,
        'cartItemsCount': cart_obj.cart_items.count()
    }


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return JsonResponse(_get_cart_detail(cart_obj))


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    new_quantity = request.POST.get('new_quantity')

    if product_id is not None and new_quantity is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('Show message to user, product is gone?')
            return redirect('cart:home')

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if 0 < int(new_quantity) <= product_obj.quantity:
            cart_item, created = cart_obj.cart_items.get_or_create(product=product_obj)
            cart_item.quantity = int(new_quantity)
            cart_item.save()
        elif int(new_quantity) <= 0:
            cart_obj.cart_items.filter(product=product_obj).delete()
        request.session['cart_items'] = cart_obj.cart_items.count()
    return redirect('cart:home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.cart_items.count() == 0:
        return redirect('cart:home')

    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()
    address_id = request.session.get('address_id', None)
    address_required = cart_obj.delivery
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    address_qs = None
    has_card = False
    order_obj = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if address_id:
            order_obj.address = Address.objects.get(id=address_id)
            del request.session['address_id']
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, orderID = billing_profile.charge('S', order_obj)
            if did_charge == 'succeeded':
                order_obj.mark_paid()  # sort signal
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect(reverse('cart:success', kwargs={'orderID': orderID}))
            else:
                return redirect('cart:checkout')

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        'has_card': has_card,
        'publish_key': STRIPE_PUB_KEY,
        'address_required': address_required,
    }
    return render(request, 'carts/checkout.html', context)


def paypal_checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.cart_items.count() == 0:
        return redirect('cart:home')

    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()
    address_id = request.session.get('address_id', None)
    address_required = cart_obj.delivery
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    address_qs = None
    has_card = False
    order_obj = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if address_id:
            order_obj.address = Address.objects.get(id=address_id)
            del request.session['address_id']
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            order_done = CreateOrder(order_obj, cart_obj)
            response = order_done.get_response()
            if response.status_code == 201 and response.result.status == 'CREATED':
                did_charge, orderID = billing_profile.charge('P', order_obj, response)
                if did_charge:
                    order_obj.mark_paid()  # sort signal
                    request.session['cart_items'] = 0
                    del request.session['cart_id']
                    return redirect(reverse('cart:success', kwargs={'orderID': orderID}))
                else:
                    return redirect('cart:checkout')

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        'has_card': has_card,
        'address_required': address_required,
    }
    return render(request, 'carts/checkout.html', context)


def checkout_done_view(request, orderID=None):
    return render(request, 'carts/checkout-done.html', {'orderID': orderID})
