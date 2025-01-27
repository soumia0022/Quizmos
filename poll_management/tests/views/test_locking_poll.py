from django.test import TestCase, Client
from user_management.models.user_model import User
from django.urls import reverse
from poll_management.models.poll_model import Poll

class PollLockTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='johndoe', password='Password123')

        # Create a sample poll
        self.poll = Poll.objects.create(
            title="Sample Poll",
            user=User.objects.get(username='johndoe'),
        )

        self.lock_url = reverse('poll_management:poll_lock', args=[self.poll.id])  # Replace namespace if different

    def test_poll_lock_get_request(self):
        """Test the GET request for poll_lock view."""
        response = self.client.get(self.lock_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lock_poll_confirmation.html')

    def test_poll_lock_post_lock(self):
        """Test the POST request to lock a poll."""
        response = self.client.post(self.lock_url, {'action': 'lock'})

        self.poll.refresh_from_db()
        self.assertTrue(self.poll.locked)
        self.assertEqual(self.poll.status, 'closed')
        self.assertRedirects(response, reverse('user_management:dashboard'))

    def test_poll_lock_post_unlock(self):
        """Test the POST request to unlock a poll."""
        self.poll.locked = True
        self.poll.status = 'closed'
        self.poll.save()

        response = self.client.post(self.lock_url, {'action': 'unlock'})

        self.poll.refresh_from_db()
        self.assertFalse(self.poll.locked)
        self.assertEqual(self.poll.status, 'active')
        self.assertRedirects(response, reverse('user_management:dashboard'))

    # def test_poll_lock_requires_authentication(self):
    #     """Test that the poll_lock view requires a logged-in user."""
    #     response = self.client.get(self.lock_url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(response.url.startswith(reverse('login')))

    #somebody else can access another lecturers polls

    # def test_poll_lock_wrong_user(self):
    #     """Test that a user who does not own the poll cannot access it."""
    #     other_user = User.objects.get(username='janedoe'),
    #     self.client.login(username='janedoe', password='pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=')
    #     response = self.client.get(self.lock_url)
    #
    #     self.assertEqual(response.status_code, 404)
