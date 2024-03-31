from django.test import TestCase

from accounts.models import User
from analytics.models import ObjectViewed


class ObjectViewedTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        self.object_viewed = ObjectViewed.objects.create(user=self.user, content_type_id=1, object_id=1)

    def test_object_viewed_creation(self):
        self.assertEqual(ObjectViewed.objects.count(), 1)
        obj_viewed = ObjectViewed.objects.first()
        self.assertEqual(obj_viewed.user, self.user)
        self.assertEqual(obj_viewed.content_type_id, 1)
        self.assertEqual(obj_viewed.object_id, 1)
