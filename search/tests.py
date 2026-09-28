from django.test import TestCase, RequestFactory
from django.utils import translation

from accounts.models import User
from products.models import Product
from search import rag
from search.views import SearchProductView


class SearchProductViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        self.product1 = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99,
            featured=True,
            active=True,
            quantity=10
        )
        self.product2 = Product.objects.create(
            title='Test Product Not Featured',
            description='This is a test product not featured',
            price=30.03,
            featured=False,
            active=True,
            quantity=1
        )
        self.product3 = Product.objects.create(
            title='Test Product Not Active',
            description='This is a test product not active',
            price=3.53,
            featured=True,
            active=False,
            quantity=67
        )
        self.product4 = Product.objects.create(
            title='Test Product Not Featured Not Active',
            description='This is a test product not featured and not active',
            price=20.87,
            featured=False,
            active=False,
            quantity=6
        )

    def test_get_queryset_with_query(self):
        view = SearchProductView()
        request = self.factory.get('search', {'q': 'Product'})
        view.request = request
        queryset = view.get_queryset()
        self.assertIn(self.product1, queryset)
        self.assertIn(self.product2, queryset)
        self.assertNotIn(self.product3, queryset)
        self.assertNotIn(self.product4, queryset)

    def test_get_queryset_without_query(self):
        view = SearchProductView()
        request = self.factory.get('search')
        view.request = request
        queryset = view.get_queryset()
        self.assertIn(self.product1, queryset)
        self.assertNotIn(self.product2, queryset)
        self.assertNotIn(self.product3, queryset)
        self.assertNotIn(self.product4, queryset)

    def test_get_context_data(self):
        view = SearchProductView()
        request = self.factory.get('search', {'q': 'Product'})
        request.session = {}
        request.user = self.user
        view.request = request
        queryset = view.get_queryset()
        context = view.get_context_data(object_list=queryset)
        self.assertEqual(context['query'], 'Product')

    def test_get_context_data_with_cart_items(self):
        view = SearchProductView()
        request = self.factory.get('search', {'q': 'Product'})
        request.session = {}
        request.user = self.user
        view.request = request
        queryset = view.get_queryset()
        queryset.in_cart = True
        context = view.get_context_data(object_list=queryset)
        self.assertEqual(len(context['object_list']), 2)


class AssistantLanguageTests(TestCase):
    def setUp(self):
        Product.objects.create(title='Mel de Urze - Heather Honey', price=9.90, quantity=5,
                               description='Dark heather honey.', description_pt='Mel de urze escuro.')

    def test_answer_follows_the_page_language_even_when_cached(self):
        with translation.override('en'):
            english = rag.ask('mel')
        with translation.override('pt'):
            portuguese = rag.ask('mel')
        self.assertIn('pick for "mel"', english['summary'])
        self.assertIn('sugestão para "mel"', portuguese['summary'])

    def test_portuguese_description_is_searchable(self):
        with translation.override('pt'):
            result = rag.ask('escuro')
        self.assertEqual([item['product'].title for item in result['products']], ['Mel de Urze - Heather Honey'])
