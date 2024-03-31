from django.test import TestCase

from marketing.forms import MarketingPreferenceForm


class MarketingPreferenceFormTest(TestCase):
    def test_form_fields(self):
        form = MarketingPreferenceForm()
        self.assertIn('subscribed', form.fields)
        self.assertFalse(form.fields['subscribed'].required)

    def test_form_valid_data(self):
        form_data = {'subscribed': True}
        form = MarketingPreferenceForm(data=form_data)
        self.assertTrue(form.is_valid())
