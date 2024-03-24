from unittest import TestCase

from django.utils import timezone
from django.utils.text import slugify

from tags.models import Tag


class TagsModelTest(TestCase):

    def test_tag_creation(self):
        tag = Tag.objects.create(title='Test Tag 1', slug='test-tag-1')
        self.assertEqual(tag.title, 'Test Tag 1')
        self.assertTrue(tag.active)
        self.assertLess(tag.timestamp, timezone.now())

    def test_tag_str_method(self):
        tag = Tag.objects.create(title='Test Tag 2', slug='test-tag-2')
        self.assertEqual(str(tag), tag.title)

    def test_tag_slug_auto_generation(self):
        tag = Tag.objects.create(title='Test Tag 3')
        self.assertIn(slugify(tag.title), tag.slug)

    def test_tag_pre_save_signal(self):
        tag = Tag.objects.create(title='Another Test Tag', slug='another-test-tag')
        tag.slug = ''
        tag.save()
        self.assertIn(slugify(tag.title), tag.slug)