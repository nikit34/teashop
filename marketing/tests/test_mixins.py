from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import User
from marketing.views import MailchimpWebhookView


class CsrfExemptMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def test_csrf_exempt_for_get_request(self):
        request = self.factory.get(reverse('webhooks-mailchimp'))
        view = MailchimpWebhookView.as_view()
        response = view(request)
        self.assertNotIn('csrftoken', response.cookies)

    def test_csrf_exempt_for_post_request(self):
        request = self.factory.post(reverse('webhooks-mailchimp'))
        request.user = self.user
        view = MailchimpWebhookView.as_view()
        response = view(request)
        self.assertNotIn('csrftoken', response.cookies)
