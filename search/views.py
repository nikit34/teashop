from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from carts.models import Cart
from products.models import Product

from .hybrid import hybrid_search
from .rag import ask


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
        query = self.request.GET.get('q', None)
        if query is not None:
            return hybrid_search(query)
        return list(Product.objects.featured())


def rag_ask_view(request):
    query = request.GET.get('q', '').strip()
    result = None
    if query:
        result = ask(query)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_product_ids = {cart_item.product_id for cart_item in cart_obj.cart_items.all()}
        for item in result['products']:
            item['product'].in_cart = item['product'].id in cart_product_ids

    if request.GET.get('format') == 'json':
        return JsonResponse({
            'query': query,
            'summary': result['summary'] if result else '',
            'products': [
                {
                    'id': item['product'].id,
                    'title': item['product'].title,
                    'price': str(item['product'].price),
                    'url': item['product'].get_absolute_url(),
                    'explanation': item['explanation'],
                }
                for item in (result['products'] if result else [])
            ],
            'clarifying_question': result.get('clarifying_question') if result else None,
            'clarifying_options': result.get('clarifying_options') if result else [],
            'insufficient_data': result['insufficient_data'] if result else True,
            'diagnostics': result['diagnostics'] if result else {},
        })

    return render(request, 'search/ask.html', {
        'query': query,
        'result': result,
    })
