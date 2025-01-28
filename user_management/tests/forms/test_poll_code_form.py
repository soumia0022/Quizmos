from django.test import TestCase
from user_management.forms import PollCodeForm
from user_management.models import User
from poll_management.models.poll_model import Poll

class PollCodeFormTest(TestCase):
    fixtures = ['user_management/tests/fixtures/default_user.json']
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.poll = Poll.objects.create(title='Test Poll', user= self.user, number_code='123456')

    def test_form_valid_data(self):
        form = PollCodeForm(data={'poll_code': '123456'})

        self.assertTrue(form.is_valid())
        valid, poll = form.validate_and_redirect()
        self.assertTrue(valid)
        self.assertEqual(poll, self.poll)

    def test_form_with_default_code(self):
        form = PollCodeForm(data={'poll_code': '0'})
        self.assertFalse(form.is_valid())
        self.assertIn('poll_code', form.errors)
        self.assertEqual(form.errors['poll_code'], ['Ensure this value has at least 6 characters (it has 1).'])

    def test_form_with_empty_data(self):
        form = PollCodeForm(data={'poll_code': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('poll_code', form.errors)

    def test_form_with_invalid_code(self):
        form = PollCodeForm(data={'poll_code': '654321'})
        self.assertTrue(form.is_valid())
        valid, poll = form.validate_and_redirect()
        self.assertFalse(valid)
        self.assertIsNone(poll)
        self.assertIn('poll_code', form.errors)
        self.assertEqual(form.errors['poll_code'], ['Invalid poll code'])
