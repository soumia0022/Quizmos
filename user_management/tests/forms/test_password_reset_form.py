from django.test import TestCase, RequestFactory, Client
from user_management.forms.forgot_password_forms import CustomPasswordResetForm, CustomSetPasswordForm
from user_management.models import User
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import re

class CustomPasswordResetFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_clean_email_registered_user(self):
        form = CustomPasswordResetForm(data={'email': 'testuser@example.com'})
        self.assertTrue(form.is_valid())

    def test_clean_email_unregistered_user(self):
            form = CustomPasswordResetForm(data={'email': 'nonexistinguser@example.com'})
            self.assertTrue(form.is_valid())
            form.save(self.factory.get('/'))
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn('You are not registered. Click the link to sign up: http://testserver/sign_up/', mail.outbox[0].body)
    
    def test_save_with_registered_user(self):
        form = CustomPasswordResetForm(data={'email': 'testuser@example.com'})
        request = self.factory.get('/')
        request.user = self.user
        request.session = self.client.session  
        form.is_valid()
        form.save(request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Click the link to reset your password', mail.outbox[0].body)

    def test_reset_password_with_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        form = CustomPasswordResetForm()
        request = self.factory.get('/')
        request.session = self.client.session  
        result = form.reset_password(uid, token, 'newpassword123', request)
        self.assertTrue(result)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_reset_password_with_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = 'invalid-token'
        form = CustomPasswordResetForm()
        request = self.factory.get('/')
        request.session = self.client.session  
        result = form.reset_password(uid, token, 'newpassword123', request)
        self.assertFalse(result)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('newpassword123'))


class CustomSetPasswordFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.factory = RequestFactory()
        self.client = Client()

    def test_clean_passwords_match(self):
        form = CustomSetPasswordForm(data={'new_password': 'NewValidPassword123', 'new_password_confirm': 'NewValidPassword123'})
        self.assertTrue(form.is_valid())

    def test_clean_passwords_do_not_match(self):
        form = CustomSetPasswordForm(data={'new_password': 'NewValidPassword123', 'new_password_confirm': 'MismatchPassword123'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["new_password"], ["Passwords do not match."])
        self.assertEqual(form.errors["new_password_confirm"], ["Passwords do not match."])

    def test_clean_password_too_short(self):
        form = CustomSetPasswordForm(data={'new_password': 'short', 'new_password_confirm': 'short'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["new_password"], ["Password must be at least 8 characters long, contain one number, one uppercase, and one lowercase letter."])
        self.assertEqual(form.errors["new_password_confirm"], ["Password must be at least 8 characters long, contain one number, one uppercase, and one lowercase letter."])
    
    def test_clean_password_missing_fields(self):
        form = CustomSetPasswordForm(data={'new_password': '', 'new_password_confirm': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["new_password"], ["This field is required.", "Both password fields are required."])
        self.assertEqual(form.errors["new_password_confirm"], ["This field is required.", "Both password fields are required."])

    def test_save_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        form = CustomSetPasswordForm(data={'new_password': 'NewValidPassword123', 'new_password_confirm': 'NewValidPassword123'})
        request = self.factory.get('/')
        request.session = self.client.session  
        form.is_valid()
        result = form.save(uid, token, request)
        self.assertTrue(result)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewValidPassword123'))

    def test_save_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = 'invalid-token'
        form = CustomSetPasswordForm(data={'new_password': 'NewValidPassword123', 'new_password_confirm': 'NewValidPassword123'})
        request = self.factory.get('/')
        request.session = self.client.session  
        form.is_valid()
        result = form.save(uid, token, request)
        self.assertFalse(result)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('NewValidPassword123'))
