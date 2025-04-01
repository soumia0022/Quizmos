from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import User
from poll_management.models.poll_model import Poll
from django.utils.timezone import now


class StudentPollsPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            role='Student'
        )
        self.polls = [
            Poll.objects.create(
                title=f"Poll {i}",
                number_code=f"{123450 + i}",
                user=self.user,
                created_at=now()
            ) for i in range(1, 15)  
        ]

    def test_student_polls_page_requires_login(self):
        """Test that unauthenticated users are redirected to the login page."""
        response = self.client.get(reverse('user_management:student_polls_page'))
        self.assertRedirects(
            response,
            f"{reverse('user_management:log_in')}?next={reverse('user_management:student_polls_page')}"
        )

    def test_student_polls_page_renders_correct_template(self):
        """Test that the page renders correctly for authenticated users."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_management:student_polls_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_polls_page.html')

    def test_student_polls_search_filter(self):
        """Test that polls are filtered by the search query."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_management:student_polls_page') + '?search=Poll 1')
        self.assertEqual(response.status_code, 200)

        filtered_polls = response.context['polls']
        self.assertTrue(all('Poll 1' in poll.title for poll in filtered_polls))

    def test_student_polls_sort_by_title_asc(self):
        """Test that polls are sorted by title in ascending order."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_management:student_polls_page') + '?sort_by=title_asc')
        self.assertEqual(response.status_code, 200)

        polls = list(response.context['polls'])
        sorted_titles = [poll.title for poll in polls]
        self.assertEqual(sorted_titles, sorted(sorted_titles))  

    def test_student_polls_sort_by_title_desc(self):
        """Test that polls are sorted by title in descending order."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_management:student_polls_page') + '?sort_by=title_desc')
        self.assertEqual(response.status_code, 200)

        polls = list(response.context['polls'])
        sorted_titles = [poll.title for poll in polls]
        self.assertEqual(sorted_titles, sorted(sorted_titles, reverse=True))  
