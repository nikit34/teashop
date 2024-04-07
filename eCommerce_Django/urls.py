from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.views.static import serve

from accounts.views import LoginView, RegisterView, GuestRegisterView
from addresses.views import (
    checkout_address_create_view,
    checkout_address_reuse_view
)
from analytics.views import SalesView, SalesAjaxView
from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_detail_api_view, checkout_api_view  # , paypal_checkout_home TODO: PayPal
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import CollectionView
from .sitemaps import global_maps, RobotsTxtView
from .views import ProductListView, about_page, contact_page, update


urlpatterns = [
    path('update_server/', update, name='update'),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    # path('cart/create-paypal-transaction/', paypal_checkout_home, name='paypal-checkout'), TODO: PayPal
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    path('api/', include(('apis.urls', 'eCommerce_Django'), namespace='apis')),

    path('sitemap.xml', sitemap, {'sitemaps': global_maps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', RobotsTxtView.as_view()),

    path("__debug__/", include("debug_toolbar.urls")),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

  ] + i18n_patterns(

    path('i18n/', include('django.conf.urls.i18n')),

    path('', ProductListView.as_view(), name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/guest/', GuestRegisterView.as_view(), name='guest_register'),
    path('collection/', CollectionView.as_view(), name='collection'),
    path('search/', include(('search.urls', 'eCommerce_Django'), namespace='search')),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),

    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include(('accounts.urls', 'eCommerce_Django'), namespace='accounts')),
    path('accounts/', include('accounts.passwords.urls')),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),

    path('address/', RedirectView.as_view(url='/addresses/')),
    path('addresses/', include(('addresses.urls', 'eCommerce_Django'), namespace='addresses')),

    path('analytics/sales/', SalesView.as_view(), name='sales-analytics'),
    path('analytics/sales/data/', SalesAjaxView.as_view(), name='sales-analytics-data'),

    path('cart/', include(('carts.urls', 'eCommerce_Django'), namespace='cart')),

    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),

    path('orders/', include(('orders.urls', 'eCommerce_Django'), namespace='orders')),

    path('products/', include(('products.urls', 'eCommerce_Django'), namespace='products')),

    path('admin/', admin.site.urls),
)


# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'TeaShop'
admin.site.index_title = 'TeaShop'
admin.site.site_title = 'TeaShop'
