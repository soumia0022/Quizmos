from django.test import TestCase
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class PollModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', role='Lecturer')

    def test_poll_creation(self):
        poll = Poll.objects.create(
            title="Sample Poll",
            status="active",
            user=self.user,
            number_code=123456
        )

        self.assertEqual(poll.title, "Sample Poll")
        self.assertEqual(poll.status, "active")
        self.assertEqual(poll.user, self.user)
        self.assertEqual(poll.number_code, 123456)
        self.assertIsNotNone(poll.created_at)

    def test_poll_str_method(self):
        poll = Poll.objects.create(
            title="Sample Poll",
            status="active",
            user=self.user,
            number_code=123456
        )

        self.assertEqual(str(poll), "Sample Poll")
