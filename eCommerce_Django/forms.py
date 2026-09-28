from django import forms
from django.utils.translation import gettext_lazy


class ContactForm(forms.Form):
    fullname = forms.CharField(label=gettext_lazy("Name"), widget=forms.TextInput(attrs={"class": "form-control", "placeholder": gettext_lazy("Your full name")}))
    email = forms.EmailField(label=gettext_lazy("Email"), widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": gettext_lazy("Your contact email")}))
    content = forms.CharField(label=gettext_lazy("Message"), widget=forms.Textarea(attrs={"class": "form-control", "placeholder": gettext_lazy("Your message")}))
