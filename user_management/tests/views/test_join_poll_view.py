from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import User
from poll_management.models.poll_model import Poll


class JoinPollPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User',
            email='testuser@example.com'
        )
        self.poll = Poll.objects.create(
            title='Test Poll',
            number_code='123456', 
            user=self.user
        )

    def test_join_poll_page_requires_login(self):
        """Test that unauthenticated users are redirected to the login page."""
        response = self.client.get(reverse('user_management:join_poll_page'))
        self.assertRedirects(
            response,
            f"{reverse('user_management:log_in')}?next={reverse('user_management:join_poll_page')}"
        )

    def test_join_poll_page_renders_correct_template(self):
        """Test that the page renders correctly for authenticated users."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_management:join_poll_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'join_poll_page.html')

    def test_join_poll_valid_code_redirects_to_poll(self):
        """Test that submitting a valid poll code redirects correctly."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user_management:join_poll_page'), {'poll_code': '123456'})
        self.assertRedirects(response, reverse('poll_management:join_poll', args=['123456']))

    def test_join_poll_invalid_code_shows_error(self):
        """Test that an invalid poll code displays an error message."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user_management:join_poll_page'), {'poll_code': '999999'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid poll code')

    def test_join_poll_empty_code_shows_error(self):
        """Test that submitting an empty poll code shows a required field error."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user_management:join_poll_page'), {'poll_code': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

