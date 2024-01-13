from django.conf.urls import url

from .views import (ProductDetailSlugView, ProductDownloadView)

urlpatterns = [
  url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
  url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]
