from django.test import TestCase, Client
from django.urls import reverse

class ReturnToDashboardTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='johndoe', password='Password123')

    def test_return_to_dashboard_redirects(self):
        """
        Test that the return_to_dashboard view redirects to the dashboard.
        """
        url = reverse('return_to_dashboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_management:dashboard'))
