"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from user_management.models import User
from poll_management.models.poll_model import  Poll
class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['user_management/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='johndoe')
        self.poll = Poll.objects.create(title='Test Poll', user=self.user, number_code='123456')

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_home_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'lecturer_dashboard.html')

    def test_home_redirects_to_join_poll_with_valid_form_data(self):
        form_data = {'poll_code': '123456'}
        response = self.client.post(self.url, data=form_data)
        self.assertRedirects(response, reverse('poll_management:join_poll', kwargs={'code': '123456'}))


    def test_home_redirects_to_home_with_invalid_form_data(self):
        form_data = {'poll_code': ''}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
