from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from billing.models import BillingProfile
from .forms import AddressCheckoutForm, AddressForm
from .models import Address


class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'addresses/list.html'

    def get_queryset(self):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'addresses/update.html'
    form_class = AddressForm
    success_url = '/addresses'

    def get_queryset(self):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('addresses:main')


class AddressCreateView(LoginRequiredMixin, CreateView):
    template_name = 'addresses/update.html'
    form_class = AddressForm
    success_url = '/addresses'

    def form_valid(self, form):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        instance = form.save(commit=False)
        instance.billing_profile = billing_profile
        instance.save()
        return super(AddressCreateView, self).form_valid(form)


def checkout_address_create_view(request):
    form = AddressCheckoutForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.save()
            request.session['address_id'] = instance.id
        else:
            print('Error redirect(cart:checkout)')
            return redirect('cart:checkout')

        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('cart:checkout')


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        if request.method == 'POST':
            address = request.POST.get('address', None)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

            if address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=address)

                if qs.exists():
                    request.session['address_id'] = address
                if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect('cart:checkout')
