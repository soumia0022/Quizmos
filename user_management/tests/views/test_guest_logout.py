from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()



class LogoutAndLoginTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.client = Client()
        self.guest_user = User.objects.create_user(
            username='guestuser',
            password='password123',
            first_name='Guest'
        )


    def test_guest_user_logout_and_delete(self):

        self.client.login(username='guestuser', password='password123')


        response = self.client.get(reverse('user_management:guest_logout') + '?next=/dashboard/')


        self.assertFalse(User.objects.filter(username='guestuser').exists())
        self.assertRedirects(response, reverse('user_management:home'))


