from django.test import TestCase
from chats.forms import CommentForm


class CommentFormTestCase(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={'msg': 'This is a valid message'})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_data(self):
        form = CommentForm(data={'msg': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('msg', form.errors)

    def test_comment_form_save_method(self):
        valid_data = {'msg': 'This is a valid message'}
        form = CommentForm(data=valid_data)

        comment = form.save(commit=False)
        self.assertEqual(comment.msg, valid_data['msg'])