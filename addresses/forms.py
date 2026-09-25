from django import forms
from django.utils.translation import gettext, gettext_lazy

from .countries import countries_dict
from .models import Address


ADDRESS_LABELS = {
    'nickname': gettext_lazy('Address nickname'),
    'name': gettext_lazy('Recipient name'),
    'address_line_1': gettext_lazy('Street and number'),
    'address_line_2': gettext_lazy('Apartment, floor'),
    'postal_code': gettext_lazy('Postal code'),
    'city': gettext_lazy('City'),
}


class StyledAddressFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class AddressForm(StyledAddressFormMixin, forms.ModelForm):
    def clean_country(self):
        country_code = self.cleaned_data.get('country')
        valid_code = False
        for country_union in countries_dict:
            if country_code == country_union['code']:
                valid_code = True
        if not valid_code:
            raise forms.ValidationError(gettext('Country code is not valid'))
        return country_code

    class Meta:
        model = Address
        fields = [
            'nickname',
            'name',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'city'
        ]
        labels = ADDRESS_LABELS


class AddressCheckoutForm(StyledAddressFormMixin, forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'name',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'city'
        ]
        labels = ADDRESS_LABELS
        widgets = {
            'postal_code': forms.TextInput(attrs={'placeholder': '1100-148'}),
            'city': forms.TextInput(attrs={'placeholder': 'Lisboa'}),
        }
