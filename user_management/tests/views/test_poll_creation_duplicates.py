from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.helpers import generate_suggested_title

class PollCreationDuplicateTests(TestCase):
    def setUp(self):
        """Set up test user before each test"""
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')
        self.dashboard_url = reverse('user_management:dashboard')

    def test_create_poll_with_duplicate_name(self):

        Poll.objects.create(user=self.user, title="Duplicate Title")
        response = self.client.post(self.dashboard_url, {'title': 'Duplicate Title'})
        self.assertContains(response, "Duplicate Title (1)")
        poll_count = Poll.objects.filter(title="Duplicate Title").count()
        self.assertEqual(poll_count, 1)
        suggested_poll_count = Poll.objects.filter(title="Duplicate Title (1)").count()
        self.assertEqual(suggested_poll_count, 0)

    def test_confirm_and_create_suggested_poll(self):

        Poll.objects.create(user=self.user, title="Duplicate Title")
        response = self.client.post(self.dashboard_url, {
            'title': 'Duplicate Title',
            'confirmed': 'true'
        })
        poll_count = Poll.objects.filter(user=self.user).count()
        self.assertEqual(poll_count, 2)
        suggested_poll_exists = Poll.objects.filter(title="Duplicate Title (1)").exists()
        self.assertTrue(suggested_poll_exists)

class GenerateSuggestedTitleTests(TestCase):
    def test_unique_title(self):

        existing_titles = []
        result = generate_suggested_title("New Title", existing_titles)
        self.assertEqual(result, "New Title")

    def test_duplicate_title_suggestion(self):

        existing_titles = ["New Title"]
        result = generate_suggested_title("New Title", existing_titles)
        self.assertEqual(result, "New Title (1)")

    def test_multiple_duplicate_titles(self):

        existing_titles = ["New Title", "New Title (1)", "New Title (2)"]
        result = generate_suggested_title("New Title", existing_titles)
        self.assertEqual(result, "New Title (3)")

    def test_non_sequential_existing_numbers(self):

        existing_titles = ["New Title", "New Title (2)", "New Title (5)"]
        result = generate_suggested_title("New Title", existing_titles)
        self.assertEqual(result, "New Title (1)")

    def test_title_with_numbers_in_name(self):

        existing_titles = ["Title 2024", "Title 2024 (1)"]
        result = generate_suggested_title("Title 2024", existing_titles)
        self.assertEqual(result, "Title 2024 (2)")
