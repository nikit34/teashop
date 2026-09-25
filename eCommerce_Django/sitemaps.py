from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from django.views.generic import TemplateView

from products.models import Product


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'about',
            'contact',
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return Product.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.timestamp


global_maps = {
    'products': ProductSitemap,
    'static': StaticViewSitemap
}


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
