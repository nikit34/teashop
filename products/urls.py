from django.urls import re_path

from .views import (ProductDetailSlugView, ProductDownloadView)

urlpatterns = [
  re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
  re_path(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]
