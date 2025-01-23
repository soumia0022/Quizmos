from django.test import TestCase
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models import User

class DisplayCodeViewTest(TestCase):
     
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
     
    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.poll = Poll.objects.create(title = 'test_poll', user=self.user, status= 'active')

        

    def test_display_code(self):
        url = reverse('display_code', args=[self.poll.pk]) 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, self.poll.title) 
        self.assertContains(response, self.poll.number_code) 
        self.assertTemplateUsed(response, 'display_code.html')
