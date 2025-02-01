from django.test import TestCase, Client
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from user_management.models import User
from user_management.views.forgot_password_views import CustomPasswordResetConfirmView
from django.core import mail

class CustomPasswordResetConfirmViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpassword123')

    def test_post_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), {
            'new_password': 'Newpassword123',
            'new_password_confirm': 'Newpassword123'
        })
    
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_management:dashboard'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Newpassword123'))

    def test_post_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = 'invalid-token'
        response = self.client.post(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), {
            'new_password': 'Newpassword123',
            'new_password_confirm': 'Newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password reset link was invalid, possibly because it has already been used. Please request a <a href="">new password reset</a>.', html=True)

    def test_get_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('<form method="post"', response.content.decode('utf-8'))
        self.assertIn('name="csrfmiddlewaretoken"', response.content.decode('utf-8'))
        self.assertIn('name="new_password"', response.content.decode('utf-8'))
        self.assertIn('name="new_password_confirm"', response.content.decode('utf-8'))
        self.assertIn('type="submit"', response.content.decode('utf-8'))

    def test_get_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = 'invalid-token'
        response = self.client.get(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password reset link was invalid, possibly because it has already been used. Please request a <a href="">new password reset</a>.', html=True)

    def test_post_password_mismatch(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), {
            'new_password': 'Newpassword123',
            'new_password_confirm': 'Mismatch123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match.')

    def test_post_password_too_short(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), {
            'new_password': 'short1A',
            'new_password_confirm': 'short1A'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password must be at least 8 characters long, contain one number, one uppercase, and one lowercase letter.')

    def test_post_identical_old_new_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), {
            'new_password': 'Testpassword123',
            'new_password_confirm': 'Testpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New password cannot be the same as the old password.')

    def test_get_invalid_uid(self):
        uid = "invalid-uid"
        token = default_token_generator.make_token(self.user)
        response = self.client.get(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password reset link was invalid, possibly because it has already been used. Please request a <a href="">new password reset</a>.', html=True)
