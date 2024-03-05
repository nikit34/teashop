from django.views.generic import ListView

from carts.models import Cart
from products.models import Product


class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        for product in context['object_list']:
            for cart_item in cart_obj.cart_items.all():
                if product == cart_item.product:
                    product.in_cart = True
                    break
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query =  method_dict.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
