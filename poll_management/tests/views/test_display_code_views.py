from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll

class DisplayCodeViewTest(TestCase):
    
    def setUp(self):
        self.poll = Poll.objects.create(title = 'test_poll')

    def test_display_code(self):
        url = reverse('display_code', args=[self.poll.pk]) 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, self.poll.title) 
        self.assertContains(response, self.poll.number_code) 
        self.assertTemplateUsed(response, 'display_code.html')
