from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import User


class AccountHomeViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        test_user.save()

    def test_url_get_not_logged_in(self):
        response = self.client.get('/en/account/')
        self.assertRedirects(response, '/login/?next=/en/account/', fetch_redirect_response=False)

    def test_url_get(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get(reverse('accounts:account-home'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/')
        self.assertTemplateUsed(response, 'accounts/home.html')

    def test_correct_context(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/')
        self.assertEqual(str(response.context['user']), 'usermodeltest@gmail.com')


class AccountEmailActivateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        test_user.save()

    def test_url_get_not_logged_in(self):
        response = self.client.get('/en/account/email/resend-activation/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name_not_logged_in(self):
        response = self.client.get(reverse('accounts:resend-activation'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_not_logged_in(self):
        response = self.client.get('/en/account/email/resend-activation/')
        self.assertTemplateUsed(response, 'registration/activation-error.html')

    def test_url_get(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/email/resend-activation/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get(reverse('accounts:resend-activation'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/email/resend-activation/')
        self.assertTemplateUsed(response, 'registration/activation-error.html')


class LoginViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        test_user.save()

    def test_url_get_not_logged_in(self):
        response = self.client.get('/en/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name_not_logged_in(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_not_logged_in(self):
        response = self.client.get('/en/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_url_get(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_correct_context(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/login/')
        self.assertEqual(str(response.context['user']), 'usermodeltest@gmail.com')


class RegisterViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        test_user.save()

    def test_url_get_not_logged_in(self):
        response = self.client.get('/en/register/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name_not_logged_in(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_not_logged_in(self):
        response = self.client.get('/en/register/')
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_url_get(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/register/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/register/')
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_correct_context(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/register/')
        self.assertEqual(str(response.context['user']), 'usermodeltest@gmail.com')


class UserDetailUpdateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        test_user.save()

    def test_url_get_not_logged_in(self):
        response = self.client.get('/en/account/details/')
        self.assertRedirects(response, '/login/?next=/en/account/details/', fetch_redirect_response=False)

    def test_url_get(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/details/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get(reverse('accounts:user-update'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/details/')
        self.assertTemplateUsed(response, 'accounts/detail-update-view.html')

    def test_correct_context(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/account/details/')
        self.assertEqual(str(response.context['user']), 'usermodeltest@gmail.com')


class RegisterViewTest(TestCase):
    form = {
        'full_name': 'Ana Silva',
        'email': 'ana@example.pt',
        'password1': 'pantry-pass-2026',
        'password2': 'pantry-pass-2026',
    }

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=False)
    def test_account_is_usable_without_mail(self):
        response = self.client.post(reverse('register'), self.form)
        self.assertRedirects(response, '/login/', fetch_redirect_response=False)
        self.assertTrue(User.objects.get(email='ana@example.pt').is_active)
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(self.client.login(email='ana@example.pt', password='pantry-pass-2026'))

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=True, BASE_URL='https://pantry.carsbuyer.org')
    def test_verification_mail_links_to_the_public_host(self):
        self.client.post(reverse('register'), self.form)
        self.assertFalse(User.objects.get(email='ana@example.pt').is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('https://pantry.carsbuyer.org/', mail.outbox[0].body)
