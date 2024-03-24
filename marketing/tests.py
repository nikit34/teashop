from django.test import TestCase
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from unittest.mock import patch

from accounts.models import User
from .models import MarketingPreference, marketing_pref_create_receiver, marketing_pref_update_receiver, make_marketing_pref_receiver


class MarketingPreferenceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def test_marketing_pref_create_receiver(self):
        MarketingPreference.objects.create(user=self.user)
        with patch('marketing.models.Mailchimp.subscribe') as mock_subscribe:
            mock_subscribe.return_value = (200, {'status': 'subscribed'})
            marketing_pref_create_receiver(sender=None, instance=self, created=True)
            self.assertTrue(MarketingPreference.objects.exists())

    def test_marketing_pref_update_receiver_subscribed(self):
        marketing_pref = MarketingPreference.objects.create(user=self.user, subscribed=True)
        with patch('marketing.models.Mailchimp.subscribe') as mock_subscribe:
            mock_subscribe.return_value = (200, {'status': 'subscribed'})
            marketing_pref_update_receiver(sender=None, instance=marketing_pref)
            self.assertTrue(marketing_pref.mailchimp_subscribed)
            self.assertEqual(marketing_pref.mailchimp_msg['status'], 'subscribed')

    def test_marketing_pref_update_receiver_unsubscribed(self):
        marketing_pref = MarketingPreference.objects.create(user=self.user, subscribed=False, mailchimp_subscribed=True)
        with patch('marketing.models.Mailchimp.unsubscribe') as mock_unsubscribe:
            mock_unsubscribe.return_value = (200, {'status': 'unsubscribed'})
            marketing_pref_update_receiver(sender=None, instance=marketing_pref)
            self.assertFalse(marketing_pref.mailchimp_subscribed)
            self.assertEqual(marketing_pref.mailchimp_msg['status'], 'unsubscribed')

    def test_make_marketing_pref_receiver(self):
        user = User.objects.create_user(
            email='newusermodeltest@gmail.com',
            full_name='New Test',
            password='test'
        )
        make_marketing_pref_receiver(sender=None, instance=user, created=True)
        self.assertTrue(MarketingPreference.objects.filter(user=user).exists())

    def test_str_method(self):
        marketing_pref = MarketingPreference.objects.create(user=self.user)
        self.assertEqual(str(marketing_pref), self.user.email)

    def tearDown(self):
        MarketingPreference.objects.all().delete()


post_save.disconnect(marketing_pref_create_receiver, sender=MarketingPreference)
pre_save.disconnect(marketing_pref_update_receiver, sender=MarketingPreference)
post_save.disconnect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)