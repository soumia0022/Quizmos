from django.test import TestCase
from django.urls import reverse

class FaqViewTest(TestCase):
    
    def test_faq_view_status_code(self):
        response = self.client.get(reverse('user_management:faq'))
        self.assertEqual(response.status_code, 200)
    
    def test_faq_view_template(self):
        response = self.client.get(reverse('user_management:faq'))
        self.assertTemplateUsed(response, 'faq.html')
    
    def test_faq_view_context(self):
        response = self.client.get(reverse('user_management:faq'))
        self.assertIn('faqs', response.context)
        faqs = response.context['faqs']
        
        self.assertIn('general', faqs)
        self.assertGreater(len(faqs['general']), 0)
        
        self.assertIn('students', faqs)
        self.assertGreater(len(faqs['students']), 0)
        
        self.assertIn('lecturers', faqs)
        self.assertGreater(len(faqs['lecturers']), 0)
