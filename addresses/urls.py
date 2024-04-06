from django.urls import path, re_path

from .views import (
    AddressListView,
    AddressCreateView,
    AddressUpdateView,
    AddressDeleteView
)


urlpatterns = [
    path('', AddressListView.as_view(), name='main'),
    path('create/', AddressCreateView.as_view(), name='create'),
    re_path(r'^(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='update'),
    re_path(r'^(?P<pk>\d+)/delete/$', AddressDeleteView.as_view(), name='delete'),
]