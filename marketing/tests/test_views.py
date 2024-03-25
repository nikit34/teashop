from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save, pre_save
from django.test import TestCase, RequestFactory

from accounts.models import User
from billing.models import user_created_receiver
from eCommerce_Django import settings
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from marketing.models import MarketingPreference, marketing_pref_update_receiver, make_marketing_pref_receiver
from unittest.mock import patch


class MarketingPreferenceUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_redirect_unauthenticated_user(self):
        request = self.factory.get(reversed('marketing-pref'))
        request.user = AnonymousUser()
        response = MarketingPreferenceUpdateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/settings/email/')

    def test_get_object(self):
        request = self.factory.get(reversed('marketing-pref'))
        user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        request.user = user
        response = MarketingPreferenceUpdateView.as_view()(request)
        self.assertEqual(response.context_data['object'].user, user)


class MailchimpWebhookViewTest(TestCase):
    @patch('marketing.views.Mailchimp')
    def test_post(self, mock_mailchimp):
        mock_mailchimp.return_value.list_id = 'test_list_id'
        mock_mailchimp.return_value.check_substription_status.return_value = (200, {'status': 'subscribed'})
        mock_mailchimp.return_value.change_substription_status.return_value = (200, {'status': 'subscribed'})

        user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        MarketingPreference.objects.create(user=user, subscribed=True, mailchimp_subscribed=False)

        request = RequestFactory().post(reversed('webhooks-mailchimp'))
        request.user = user

        response = MailchimpWebhookView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/en/')

        preference = MarketingPreference.objects.get(user=user)
        self.assertTrue(preference.subscribed)
        self.assertFalse(preference.mailchimp_subscribed)


post_save.disconnect(user_created_receiver, sender=User)
pre_save.disconnect(marketing_pref_update_receiver, sender=MarketingPreference)
post_save.disconnect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)