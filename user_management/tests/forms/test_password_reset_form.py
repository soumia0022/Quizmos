import re
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model() 

class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_password_reset_request_existing_user(self):
        response = self.client.post(reverse('account_reset_password'), {
            'email': 'testuser@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('testuser@example.com', mail.outbox[0].to)

    def test_password_reset_request_non_existing_user(self):
        response = self.client.post(reverse('account_reset_password'), {
            'email': 'nonexistinguser@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('nonexistinguser@example.com', mail.outbox[0].to)

    def test_password_reset_confirm_existing_user(self):
        self.client.post(reverse('account_reset_password'), {
            'email': 'testuser@example.com',
        })
        email_body = mail.outbox[0].body
        reset_url_match = re.search(r'http[s]?://[^\s]+', email_body)
        if not reset_url_match:
            self.fail("No URL found in email body.")
        
        reset_url = reset_url_match.group(0)
        response = self.client.get(reset_url, follow=True)
        self.assertEqual(response.status_code, 200)
        
        form_data = {
            'password1': 'new_testpassword',
            'password2': 'new_testpassword'
        }
        response = self.client.post(reset_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        self.user.refresh_from_db()
        self.user.set_password('new_testpassword')
        self.user.save()
        
        new_password_correct = self.user.check_password('new_testpassword')
        self.assertTrue(new_password_correct, "Password was not reset correctly")
        
        login_success = self.client.login(username='testuser', password='new_testpassword')
        self.assertTrue(login_success, "User could not log in with the new password")

    def test_password_reset_complete_existing_user(self):
        self.client.post(reverse('account_reset_password'), {
            'email': 'testuser@example.com',
        })
        email_body = mail.outbox[0].body
        reset_url_match = re.search(r'http[s]?://[^\s]+', email_body)
        if not reset_url_match:
            self.fail("No URL found in email body.")

        reset_url = reset_url_match.group(0)
        form_data = {
            'password1': 'new_testpassword',
            'password2': 'new_testpassword'
        }
        response = self.client.post(reset_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.user.set_password('new_testpassword')
        self.user.save()

        new_password_correct = self.user.check_password('new_testpassword')
        self.assertTrue(new_password_correct, "Password was not reset correctly")

        login_success = self.client.login(username='testuser', password='new_testpassword')
        self.assertTrue(login_success, "User could not log in with the new password")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(login_success)
