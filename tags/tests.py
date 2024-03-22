from unittest import TestCase

from django.utils import timezone
from django.utils.text import slugify

from tags.models import Tag


class TagsModelTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(title='Test Tag 1', slug='test-tag-1')
        self.tag2 = Tag.objects.create(title='Test Tag 2', slug='test-tag-2')

    def test_tag_creation(self):
        self.assertEqual(self.tag1.title, 'Test Tag 1')
        self.assertEqual(self.tag2.title, 'Test Tag 2')
        self.assertTrue(self.tag1.active)
        self.assertTrue(self.tag2.active)
        self.assertLess(self.tag1.timestamp, timezone.now())
        self.assertLess(self.tag2.timestamp, timezone.now())

    def test_tag_str_method(self):
        self.assertEqual(str(self.tag1), self.tag1.title)
        self.assertEqual(str(self.tag2), self.tag2.title)

    def test_tag_slug_auto_generation(self):
        tag3 = Tag.objects.create(title='Test Tag 3')
        self.assertTrue(slugify(tag3.title) in tag3.slug)

    def test_tag_pre_save_signal(self):
        tag4 = Tag.objects.create(title='Test Tag 4')
        self.assertTrue(slugify(tag4.title) in tag4.slug)

        tag5 = Tag.objects.create(title='Another Test Tag', slug='another-test-tag')
        tag5.slug = ''
        tag5.save()
        self.assertTrue(slugify(tag5.title) in tag5.slug)