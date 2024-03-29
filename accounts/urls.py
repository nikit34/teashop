from django.urls import path, re_path

from products.views import UserProductHistoryView
from .views import (
    AccountHomeView,
    AccountEmailActivateView,
    UserDetailUpdateView
)

urlpatterns = [
    path('', AccountHomeView.as_view(), name='account-home'),
    path('details/', UserDetailUpdateView.as_view(), name='user-update'),
    path('history/products/', UserProductHistoryView.as_view(), name='user-product-history'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),
]
