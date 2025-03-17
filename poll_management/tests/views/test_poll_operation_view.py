from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models import User

class PollOperationsTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.student_user = User.objects.create_user(username='student', password='Password123', role='Student')
        self.client = Client()
        self.client.login(username='johndoe', password='Password123')
        self.poll = Poll.objects.create(title='Test Poll', user=self.user, status='active')

    
    def test_edit_poll(self):
        response = self.client.post(reverse('poll_management:poll_edit', args=[self.poll.pk]), {
            'title': 'Updated Poll Title',
            'status': 'closed'
        })
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.title, 'Updated Poll Title')
        self.assertEqual(self.poll.status, 'closed')
        self.assertRedirects(response, reverse('poll_management:view_poll', args=[self.poll.pk]))
    
    def test_edit_poll_get_request(self):
        """Test if accessing poll_edit via GET renders the correct template."""
        response = self.client.get(reverse('poll_management:poll_edit', args=[self.poll.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll_edit.html')
        self.assertEqual(response.context['poll'], self.poll)
    
    def test_delete_poll(self):
        response = self.client.post(reverse('poll_management:poll_delete', args=[self.poll.pk]))
        self.assertFalse(Poll.objects.filter(id=self.poll.pk).exists())
        self.assertRedirects(response, reverse('user_management:dashboard'))
    
    def test_delete_poll_get_request(self):
        """Test if sending a GET request to poll_delete does not delete the poll and redirects properly."""
        response = self.client.get(reverse('poll_management:poll_delete', args=[self.poll.pk]))
        self.assertTrue(Poll.objects.filter(id=self.poll.pk).exists())
        self.assertRedirects(response, reverse('user_management:dashboard'))
    
    def test_view_poll_not_found(self):
        response = self.client.get(reverse('poll_management:view_poll', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_edit_poll_not_found(self):
        response = self.client.post(reverse('poll_management:poll_edit', args=[999]), {
            'title': 'Updated Poll Title',
            'status': 'closed'
        })
        self.assertEqual(response.status_code, 404)
    
    def test_delete_poll_not_found(self):
        response = self.client.post(reverse('poll_management:poll_delete', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_student_removes_joined_poll(self):
        """Test if a student user can remove a poll from their joined polls."""
        self.client.logout()
        self.client.login(username='student', password='Password123')
        self.student_user.joined_polls.add(self.poll)
        response = self.client.post(reverse('poll_management:poll_delete', args=[self.poll.pk]))
        self.assertTrue(Poll.objects.filter(id=self.poll.pk).exists())
        self.assertRedirects(response, reverse('user_management:dashboard'))
        self.student_user.refresh_from_db()
        self.assertFalse(self.poll in self.student_user.joined_polls.all())
