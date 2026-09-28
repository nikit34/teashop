from django.core import mail
from django.test import TestCase
from django.urls import reverse

from chats.models import ContactMessage
from products.models import Product


class RobotsTxtTests(TestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "text/plain")
        lines = response.content.decode().splitlines()
        self.assertEqual(lines[0], "User-Agent: *")


class SitemapHostTests(TestCase):
    def test_urls_use_the_requested_host(self):
        Product.objects.create(title='Mel Teste - Test Honey', price='9.90', quantity=5)
        response = self.client.get('/sitemap.xml', HTTP_HOST='pantry.carsbuyer.org')
        self.assertContains(response, 'http://pantry.carsbuyer.org/')
        self.assertNotContains(response, 'example.com')


class ContactPageTests(TestCase):
    def test_message_is_kept_even_without_mail(self):
        response = self.client.post(reverse('contact'), {
            'fullname': 'Ana Silva',
            'email': 'ana@example.pt',
            'content': 'Do you deliver a hamper to Porto before Christmas?',
        })
        self.assertEqual(response.status_code, 200)
        message = ContactMessage.objects.get()
        self.assertEqual(message.email, 'ana@example.pt')
        self.assertIn('Porto', message.content)
        self.assertEqual(len(mail.outbox), 1)


class RemovedHooksTests(TestCase):
    def test_git_pull_hook_is_gone(self):
        response = self.client.post('/update_server/')
        self.assertEqual(response.status_code, 404)
