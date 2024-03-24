from django.urls import re_path

from .views import ProductDetailSlugView

urlpatterns = [
  re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail')
]
