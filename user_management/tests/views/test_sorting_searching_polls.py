from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MultipleChoiceResponse  
from question_management.models.question_models import Question

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
    
        self.student = get_user_model().objects.create_user(
            username='student',
            email='student@example.com',
            password='password123',
            role='Student'
        )

        # Creating test polls
        self.poll1 = Poll.objects.create(
            user=self.user, 
            title="Space", 
            created_at=now() - timedelta(days=5)
        )
        self.poll2 = Poll.objects.create(
            user=self.user, 
            title="Rocket", 
            created_at=now() - timedelta(days=3)
        )
        self.poll3 = Poll.objects.create(
            user=self.user, 
            title="Stars", 
            created_at=now() - timedelta(days=1)
        )


        for poll in [self.poll1, self.poll2, self.poll3]:
            question = Question.objects.create(
                poll=poll,
                question_type="multiple_choice",
                multiple_choice_question="Dummy question?",
                multiple_choice_options=["A", "B"]
            )
            MultipleChoiceResponse.objects.create(
                user=self.student,
                poll=poll,
                question=question,
                session_code=poll.number_code,
                selected_options='["A"]'
            )
            
        self.client.login(username='testuser', password='password123')

    def test_search_polls(self):
        """Test that search returns correct results"""
        response = self.client.get('/dashboard/', {'search': 'Space'})
        self.assertContains(response, "Space")  # Should find Space
        self.assertNotContains(response, "Rocket")  # Should not find Rocket
        self.assertNotContains(response, "Stars")  # Should not find Stars

    def test_search_startswith_behavior(self):
        """Ensure search only returns polls where title starts with query"""
        response = self.client.get('/dashboard/', {'search': 'S'})
        self.assertContains(response, "Space")
        self.assertContains(response, "Stars")
        self.assertNotContains(response, "Rocket")

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


    def test_student_search_polls(self):
        """Test that search returns correct results for student dashboard"""
        self.client.login(username='student', password='password123')

        response = self.client.get('/dashboard/', {'search': 'Space'})
        self.assertContains(response, "Space")
        self.assertNotContains(response, "Rocket")
        self.assertNotContains(response, "Stars")

    def test_student_sort_title_ascending(self):
        """Test sorting A-Z for student dashboard"""
        self.client.login(username='student', password='password123')

        response = self.client.get('/dashboard/', {'sort_by': 'title_asc'})
        polls = list(response.context['polls'])
        self.assertEqual([p.title for p in polls], ["Rocket", "Space", "Stars"])

    def test_student_sort_title_descending(self):
        """Test sorting Z-A for student dashboard"""
        self.client.login(username='student', password='password123')

        response = self.client.get('/dashboard/', {'sort_by': 'title_desc'})
        polls = list(response.context['polls'])
        self.assertEqual([p.title for p in polls], ["Stars", "Space", "Rocket"])
