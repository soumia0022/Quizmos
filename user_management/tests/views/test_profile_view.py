"""Tests for the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from user_management.forms import UserForm
from user_management.models import User
from user_management.tests.helpers import reverse_with_next
from user_management.forms.update_profile import PasswordForm

class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('user_management:profile')
        self.form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'username': 'johndoe2',
            'email': 'johndoe2@example.org',
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertEqual(form.instance, self.user)

    def test_unsuccesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = 'janedoe'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_succesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('user_management:dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'lecturer_dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe2')
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe2@example.org')

    def test_guest_user_cannot_edit_profile(self):
        guest_user = User.objects.create_user(username="Guest", password="Guest123", first_name="Guest")
        self.client.login(username=guest_user.username, password="Guest123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('user_management:home'))

    def test_get_profile_redirects_when_not_logged_in(self):  
        response = self.client.get(self.url)  
        self.assertRedirects(response, reverse('user_management:home'))

    def test_post_profile_redirects_when_not_logged_in(self):
        response = self.client.post(self.url, self.form_input)  
        self.assertRedirects(response, reverse('user_management:home'))

    def test_delete_account_redirects_when_not_logged_in(self):
        """Test that trying to delete an account while not logged in redirects to login."""
        url = reverse('user_management:delete_account')
        login_url = reverse('user_management:log_in')  

        response = self.client.post(url)

        expected_redirect_url = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect_url)  

        # Ensure the user still exists
        self.assertTrue(User.objects.filter(username=self.user.username).exists())


    def test_logged_in_user_can_delete_account(self):
        """Test that a logged-in user can delete their account successfully."""
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('user_management:delete_account')
        before_count = User.objects.count()
        response = self.client.post(url, follow=True)
        after_count = User.objects.count()
        
        self.assertRedirects(response, reverse('user_management:home'))
        self.assertEqual(after_count, before_count - 1)  
        self.assertFalse(User.objects.filter(username=self.user.username).exists())  
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_guest_user_cannot_delete_account(self):
        """Test that a guest user cannot delete their account."""
        guest_user = User.objects.create_user(username="Guest", password="Guest123", first_name="Guest")
        self.client.login(username=guest_user.username, password="Guest123")

        url = reverse('user_management:delete_account')
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('user_management:home'))  
        self.assertFalse(User.objects.filter(username=guest_user.username).exists()) 

    def test_delete_account_requires_post_request(self):
        """Test that sending a GET request to delete account returns an error."""
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('user_management:delete_account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400) 
        self.assertTrue(User.objects.filter(username=self.user.username).exists())  

class PasswordViewTest(TestCase):
    """Test suite for the password change view."""

    fixtures = [
        'user_management/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('user_management:password')
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123',
        }

    def test_password_url(self):
        self.assertEqual(self.url, '/password/')

    def test_get_password_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordForm))

    def test_get_form_kwargs(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.user, self.user)

    def test_successful_password_change(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(response, reverse('user_management:dashboard'))
        self.user.refresh_from_db()
        is_password_correct = self.user.check_password('NewPassword123')
        self.assertTrue(is_password_correct)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(str(messages_list[0]), "Password updated!")

    def test_password_change_unsuccessful_with_incorrect_old_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['password'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password.html')
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.user.refresh_from_db()
        is_password_correct = self.user.check_password('Password123')
        self.assertTrue(is_password_correct)

    def test_password_view_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        login_url = reverse('user_management:log_in')
        expected_redirect_url = f"{login_url}?next={self.url}"
        self.assertRedirects(response, expected_redirect_url)




    