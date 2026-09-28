import ast
import gettext
import os

from django.conf import settings
from django.test import TestCase


def read_po(path):
    entries = []
    with open(path, encoding='utf-8') as f:
        blocks = f.read().split('\n\n')
    for block in blocks:
        fields, flags, key = {}, '', None
        for line in block.splitlines():
            if line.startswith('#,'):
                flags += line
            elif line.startswith('#'):
                continue
            elif line.startswith('"'):
                fields[key] += ast.literal_eval(line)
            elif line:
                key, _, value = line.partition(' ')
                fields[key] = ast.literal_eval(value)
        if fields.get('msgid'):
            entries.append((fields, flags))
    return entries


class PortugueseCatalogTests(TestCase):
    def test_catalogs_are_complete_and_compiled(self):
        for domain in ('django', 'djangojs'):
            po_path = os.path.join(settings.BASE_DIR, 'locale', 'pt', 'LC_MESSAGES', domain + '.po')
            with open(po_path[:-2] + 'mo', 'rb') as f:
                compiled = gettext.GNUTranslations(f)
            entries = read_po(po_path)
            self.assertTrue(entries)
            for fields, flags in entries:
                self.assertNotIn('fuzzy', flags, fields['msgid'])
                if 'msgid_plural' in fields:
                    self.assertTrue(fields['msgstr[0]'] and fields['msgstr[1]'], fields['msgid'])
                    self.assertEqual(compiled.ngettext(fields['msgid'], fields['msgid_plural'], 1), fields['msgstr[0]'])
                else:
                    self.assertTrue(fields['msgstr'], fields['msgid'])
                    self.assertEqual(compiled.gettext(fields['msgid']), fields['msgstr'])


class LanguageRoutingTests(TestCase):
    def test_russian_is_no_longer_served(self):
        self.assertEqual(self.client.get('/ru/').status_code, 404)
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='ru')
        self.assertRedirects(response, '/en/', fetch_redirect_response=False)

    def test_portuguese_browser_lands_on_portuguese(self):
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='pt-PT,pt;q=0.9')
        self.assertRedirects(response, '/pt/', fetch_redirect_response=False)

    def test_portuguese_home_is_fully_portuguese(self):
        response = self.client.get('/pt/')
        self.assertContains(response, 'A despensa portuguesa')
        self.assertContains(response, 'Ordenar por')
        self.assertNotContains(response, 'Sort by')
        self.assertNotContains(response, 'Gift hampers')

    def test_javascript_strings_are_translated(self):
        response = self.client.get('/pt/jsi18n/')
        self.assertContains(response, 'No carrinho')
        self.assertContains(response, 'A pesquisar...')


class SitemapLanguageTests(TestCase):
    def test_lists_both_languages_with_alternates(self):
        response = self.client.get('/sitemap.xml', HTTP_HOST='pantry.carsbuyer.org')
        self.assertContains(response, 'http://pantry.carsbuyer.org/pt/about/')
        self.assertContains(response, 'http://pantry.carsbuyer.org/en/about/')
        self.assertContains(response, 'hreflang="pt"')
        self.assertContains(response, 'hreflang="x-default"')
        self.assertNotContains(response, '/ru/')
