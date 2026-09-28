from django import forms
from django.utils.translation import gettext_lazy

from .models import Comment, WaitlistSignup


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('msg',)


class WaitlistForm(forms.ModelForm):
    class Meta:
        model = WaitlistSignup
        fields = ('email', 'name', 'occasion', 'company', 'boxes')
        labels = {
            'email': gettext_lazy('Email'),
            'name': gettext_lazy('Name'),
            'occasion': gettext_lazy('Who is it for?'),
            'company': gettext_lazy('Company, if it is for your company'),
            'boxes': gettext_lazy('How many boxes would you need?'),
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}),
            'occasion': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'organization'}),
            'boxes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 1000}),
        }
