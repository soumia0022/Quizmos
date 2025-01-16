from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll

class CreatePollViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('create_poll')

    def test_create_poll_view_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_poll.html')

    def test_create_poll_view_post(self):
        data = {
            'title': 'Sample Poll'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        poll = Poll.objects.get(title='Sample Poll')
        self.assertIsNotNone(poll)
        # self.assertRedirects(response, reverse('add_question', kwargs={'poll_id': poll.id})) # Uncomment this when the 'add_question' URL is available
