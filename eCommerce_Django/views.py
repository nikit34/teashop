import git
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from carts.models import Cart
from products.models import Product, Category
from .forms import ContactForm


class ProductListView(ListView):
    template_name = 'main/home_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)

        context['categories'] = Category.objects.all()
        context['active_category'] = self._active_category()
        context['sort'] = self.request.GET.get('sort', 'recommended')
        context['products_count'] = len(context['object_list'])

        context['cart'] = cart_obj
        for product in context['object_list']:
            for cart_item in cart_obj.cart_items.all():
                if product == cart_item.product:
                    product.in_cart = True
                    break
        return context

    def _active_category(self):
        value = self.request.GET.get('category')
        if not value or value in ('reset', 'all'):
            return None
        return Category.objects.filter(slug=value).first() or Category.objects.filter(name=value).first()

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category')

        category = self._active_category()
        if category is not None:
            queryset = queryset.filter(category=category)

        sort = self.request.GET.get('sort')
        price_order = self.request.GET.get("price")
        time_order = self.request.GET.get("time_update")
        if sort == 'price_asc' or price_order == "ascend":
            return queryset.order_by('price')
        if sort == 'price_desc' or price_order == "descend":
            return queryset.order_by('-price')
        if sort == 'newest' or time_order == "descend":
            return queryset.order_by('-timestamp')
        if time_order == "ascend":
            return queryset.order_by('timestamp')
        return queryset.order_by('-featured', 'category__ordering', 'title')


def about_page(request):
    context = {
        "title": gettext("About"),
        "content": gettext("Welcome to about page!")
    }
    return render(request, "contact/about.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    support_email = getattr(settings, 'SUPPORT_EMAIL', None)
    context = {
        "title": gettext("Contact"),
        "content": gettext("Here you can leave your feedback."),
        "form": contact_form,
    }
    if contact_form.is_valid():
        fullname = contact_form.cleaned_data['fullname']
        email = contact_form.cleaned_data['email']
        content = contact_form.cleaned_data['content']
        msg_content = gettext('Send with contact email: ') + email + '\n\n' + content
        try:
            send_mail(fullname, msg_content, email, [support_email])
        except BadHeaderError:
            return HttpResponse(gettext('Invalid header found.'))
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'message': gettext('Thank you for your submission')})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse(errors, status=400, content_type='application/json')
    return render(request, "contact/view.html", context)


@csrf_exempt
def update(request):
    if request.method == 'POST':
        repo = git.Repo('/home/TeaShop/teashop.pythonanywhere.com/.git/')
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse(gettext("Update code on server"))
    else:
        return HttpResponse(gettext("ERROR: Could`t update the code on server"))
