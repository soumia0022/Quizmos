from django.test import TestCase
from django.urls import reverse

class AboutViewTest(TestCase):
    
    def test_about_view_status_code(self):
        response = self.client.get(reverse('user_management:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view_template(self):
        response = self.client.get(reverse('user_management:about'))
        self.assertTemplateUsed(response, 'about.html')
    
    def test_about_view_context(self):
        response = self.client.get(reverse('user_management:about'))
        self.assertIn('mission', response.context)
        self.assertIn('journey', response.context)
        self.assertIn('features', response.context)
        self.assertIn('values', response.context)
        self.assertIn('team', response.context)
        self.assertIn('reviews', response.context)
      