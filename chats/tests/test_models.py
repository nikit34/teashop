from django.utils import timezone
from django.test import TestCase
from accounts.models import User
from chats.models import Comment
from products.models import Product


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99
        )
        self.comment = Comment.objects.create(
            listing=self.product,
            msg='Test comment',
            sender=self.user,
            send_time=timezone.now(),
            active=True
        )

    def test_comment_str_representation(self):
        expected_str = f'Comment {self.comment.msg} by {self.comment.sender}'
        self.assertEqual(str(self.comment), expected_str)

    def test_comment_ordering(self):
        Comment.objects.create(
            listing=self.product,
            msg='Another test comment',
            sender=self.user,
            send_time=timezone.now() + timezone.timedelta(minutes=5),
            active=True
        )

        comments = Comment.objects.filter(listing=self.product)
        self.assertLess(comments[0].send_time, comments[1].send_time)

    def test_comment_related_name(self):
        comments = self.product.comments.all()
        self.assertIn(self.comment, comments)

    def test_comment_deletion_cascade(self):
        self.product.delete()
        comments = Comment.objects.filter(pk=self.comment.pk)
        self.assertFalse(comments.exists())

    def test_comment_sender_deletion_behavior(self):
        new_user = User.objects.create_user(
            email='new_usermodeltest@gmail.com',
            full_name='New Test',
            password='test'
        )
        self.comment.sender = new_user
        self.comment.save()
        self.assertEqual(self.comment.sender, new_user)
