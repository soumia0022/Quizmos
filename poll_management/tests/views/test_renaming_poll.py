from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class RenamePollTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='johndoe', password='Password123')

        # Create a sample poll
        self.poll = Poll.objects.create(
            title="Original Poll Title",
            user=User.objects.get(username='johndoe'),
        )

        # Define the URL for adding a question (which also allows renaming the poll)
        self.add_question_url = reverse('question_management:add_question', kwargs={'poll_id': self.poll.id})

    def test_rename_poll_successfully(self):
        """
        Test renaming a poll successfully when adding a question.
        """
        new_title = "Updated Poll Title"
        data = {
            'poll_title': new_title,  # New title provided
        }

        response = self.client.post(self.add_question_url, data)

        # Expect a redirect (302 status code)
        self.assertEqual(response.status_code, 302)

        # Verify the redirection URL is correct (back to the poll's add question page)
        self.assertRedirects(response, self.add_question_url)

        # Verify the poll's title has been updated
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.title, new_title)  # Ensure title updated

    def test_rename_poll_using_hidden_field(self):
        """
        Test renaming a poll using the hidden field 'poll_title_hidden'.
        """
        new_title = "Hidden Poll Title"
        data = {
            'poll_title_hidden': new_title,  # New title provided via hidden field
        }

        response = self.client.post(self.add_question_url, data)

        # Expect a redirect (302 status code)
        self.assertEqual(response.status_code, 302)

        # Verify the redirection URL is correct (back to the poll's add question page)
        self.assertRedirects(response, self.add_question_url)

        # Verify the poll's title has been updated
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.title, new_title)

    def test_rename_poll_no_title_change(self):
        """
        Test that if no new title is provided, the poll title remains unchanged.
        """
        data = {}  # No new title provided

        response = self.client.post(self.add_question_url, data)

        # Expect a redirect (302 status code)
        self.assertEqual(response.status_code, 302)

        # Verify the redirection URL is correct (back to the poll's add question page)
        self.assertRedirects(response, self.add_question_url)

        # Verify no change in the title
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.title, "Original Poll Title")  # Ensure title did not change

    def test_rename_poll_title_already_set(self):
        """
        Test that renaming the poll to the same existing title does nothing.
        """
        data = {
            'poll_title': "Original Poll Title"  # Same title as before
        }

        response = self.client.post(self.add_question_url, data)

        # Expect a redirect (302 status code)
        self.assertEqual(response.status_code, 302)

        # Verify the redirection URL is correct (back to the poll's add question page)
        self.assertRedirects(response, self.add_question_url)

        # Verify the poll's title has not been changed
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.title, "Original Poll Title")  # Ensure title remains unchanged
