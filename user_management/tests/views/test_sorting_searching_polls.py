from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MultipleChoiceResponse  

class DashboardSortingSearchingTests(TestCase):

    def setUp(self):
        """Set up test user and test polls before each test"""
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com', 
            password='password123',
            role='Lecturer'
        )
        self.client.login(username='testuser', password='password123')

        # Creating test polls
        self.poll1 = Poll.objects.create(user=self.user, title="Space", created_at=now() - timedelta(days=5))
        self.poll2 = Poll.objects.create(user=self.user, title="Rocket", created_at=now() - timedelta(days=3))
        self.poll3 = Poll.objects.create(user=self.user, title="Stars", created_at=now() - timedelta(days=1))

    def test_search_polls(self):
        """Test that search returns correct results"""
        response = self.client.get('/dashboard/', {'search': 'Space'})
        self.assertContains(response, "Space")  # Should find Space
        self.assertNotContains(response, "Rocket")  # Should not find Rocket
        self.assertNotContains(response, "Stars")  # Should not find Stars

    def test_sort_title_ascending(self):
        """Test sorting A-Z"""
        response = self.client.get('/dashboard/', {'sort_by': 'title_asc'})
        polls = list(response.context['polls'])
        self.assertEqual([poll.title for poll in polls], ["Rocket", "Space", "Stars"])  # Sorting from A-Z

    def test_sort_title_descending(self):
        """Test sorting Z-A"""
        response = self.client.get('/dashboard/', {'sort_by': 'title_desc'})
        polls = list(response.context['polls'])
        self.assertEqual([poll.title for poll in polls], ["Stars", "Space", "Rocket"])  # Sorting from Z-A

    def test_sort_created_at_ascending(self):
        """Test sorting from oldest to newest"""
        response = self.client.get('/dashboard/', {'sort_by': 'created_at_asc'})
        polls = list(response.context['polls'])
        self.assertEqual([poll.title for poll in polls], ["Space", "Rocket", "Stars"])  # Oldest first

    def test_sort_created_at_descending(self):
        """Test sorting from newest to oldest"""
        response = self.client.get('/dashboard/', {'sort_by': 'created_at_desc'})
        polls = list(response.context['polls'])
        self.assertEqual([poll.title for poll in polls], ["Stars", "Rocket", "Space"])  # Newest first

    def create_student_user(self):
        """Helper function to create a student user with a unique email and responses"""
        student_user = get_user_model().objects.create_user(
            username='student',
            email='student@example.com', 
            password='password123',
            role='Student'
        )
        student_user.joined_polls.set([self.poll1, self.poll2, self.poll3])

        from question_management.models.question_models import Question
        q1 = Question.objects.create(poll=self.poll1, question_type='multiple_choice', multiple_choice_question="Q1")
        q2 = Question.objects.create(poll=self.poll2, question_type='multiple_choice', multiple_choice_question="Q2")
        q3 = Question.objects.create(poll=self.poll3, question_type='multiple_choice', multiple_choice_question="Q3")

        MultipleChoiceResponse.objects.create(
            question=q1,
            user=student_user,
            poll=self.poll1,
            selected_options=['Option 1'],
            session_code=123456  
        )
        MultipleChoiceResponse.objects.create(
            question=q2,
            user=student_user,
            poll=self.poll2,
            selected_options=['Option 1'],
            session_code=123456  
        )
        MultipleChoiceResponse.objects.create(
            question=q3,
            user=student_user,
            poll=self.poll3,
            selected_options=['Option 1'],
            session_code=123456 
        )
        return student_user

    def test_student_search_polls(self):
        """Test that search returns correct results for student dashboard"""
        student_user = self.create_student_user()
        self.client.login(username='student', password='password123')

        response = self.client.get('/dashboard/', {'search': 'Space'})
        self.assertContains(response, "Space")
        self.assertNotContains(response, "Rocket")
        self.assertNotContains(response, "Stars")

    def test_student_sort_title_ascending(self):
        """Test sorting A-Z for student dashboard"""
        student_user = self.create_student_user()
        self.client.login(username='student', password='password123')

        response = self.client.get('/dashboard/', {'sort_by': 'title_asc'})
        polls = list(response.context['polls'])
        self.assertEqual([p['title'] for p in polls], ["Rocket", "Space", "Stars"])

    def test_student_sort_title_descending(self):
        """Test sorting Z-A for student dashboard"""
        student_user = self.create_student_user()
        self.client.login(username='student', password='password123')

        response = self.client.get('/dashboard/', {'sort_by': 'title_desc'})
        polls = list(response.context['polls'])
        self.assertEqual([p['title'] for p in polls], ["Stars", "Space", "Rocket"])

    def test_student_sort_created_at_ascending(self):
        """Test sorting from oldest to newest for student dashboard"""
        student_user = self.create_student_user()
        self.client.login(username='student', password='password123')

        response = self.client.get('/dashboard/', {'sort_by': 'created_at_asc'})
        polls = list(response.context['polls'])
        self.assertEqual([p['title'] for p in polls], ["Space", "Rocket", "Stars"])