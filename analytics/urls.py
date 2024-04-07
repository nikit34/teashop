from django.urls import path

from carts.views import cart_detail_api_view, checkout_api_view


urlpatterns = [
    path('cart/', cart_detail_api_view, name='api-cart'),
    path('checkout/', checkout_api_view, name='api-checkout'),
]
