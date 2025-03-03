from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from poll_management.models.poll_model import Poll

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
        """Test that a user cannot create two polls with the same title directly, but gets a suggested title instead"""


        Poll.objects.create(user=self.user, title="Duplicate Title")


        response = self.client.post(self.dashboard_url, {'title': 'Duplicate Title'})


        self.assertContains(response, "Duplicate Title (1)")


        poll_count = Poll.objects.filter(title="Duplicate Title").count()
        self.assertEqual(poll_count, 1)


        suggested_poll_count = Poll.objects.filter(title="Duplicate Title (1)").count()
        self.assertEqual(suggested_poll_count, 0)

    def test_confirm_and_create_suggested_poll(self):
        """Test that when a suggested title is confirmed, the new poll gets created"""


        Poll.objects.create(user=self.user, title="Duplicate Title")


        response = self.client.post(self.dashboard_url, {
            'title': 'Duplicate Title',
            'confirmed': 'true'
        })


        poll_count = Poll.objects.filter(user=self.user).count()
        self.assertEqual(poll_count, 2)


        suggested_poll_exists = Poll.objects.filter(title="Duplicate Title (1)").exists()
        self.assertTrue(suggested_poll_exists)
