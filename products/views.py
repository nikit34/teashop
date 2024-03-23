from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import Http404, JsonResponse
from django.views.generic import ListView, DetailView

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from chats.forms import CommentForm
from chats.models import Comment
from .models import Product, ProductFile


class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "products/user-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        for product in context['object_list']:
            for cart_item in cart_obj.cart_items.all():
                if product == cart_item.product:
                    product.in_cart = True
                    break
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
        return views


class ProductListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        for product in context['object_list']:
            for cart_item in cart_obj.cart_items.all():
                if product == cart_item.product:
                    product.in_cart = True
                    break
        return context

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid() and not isinstance(request.user, AnonymousUser):
            new_comment = comment_form.save(commit=False)
            new_comment.listing = self.object
            new_comment.sender = request.user
            new_comment.save()
            context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
            return self.render_to_response(context=context)
        return JsonResponse({'error': 'Form is not valid'}, status=400)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        slug = self.kwargs.get('slug')
        slides = ProductFile.objects.all().filter(product__slug=slug)
        context['slides'] = slides
        context['comments'] = ''
        context['comment_form'] = CommentForm()
        try:
            instance = Product.objects.get(slug=slug, active=True)
            instance.views = instance.views + 1
            instance.save()
            context['views'] = instance.views
            context['comments'] = instance.comments.filter(active=True)
            context['in_cart'] = False
            for cart_item in cart_obj.cart_items.all():
                if instance == cart_item.product:
                    context['in_cart'] = True
                    break
        except Comment.DoesNotExist:
            raise Http404('Not found..')
        except:
            raise Http404('Indefinite')
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Not found..')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Indefinite')
        return instance
