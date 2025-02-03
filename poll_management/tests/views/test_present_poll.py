from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from user_management.models import User

class PollPresentationTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.poll = Poll.objects.create(title="Test Poll", number_code=123456, user = self.user)
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Test question?",
            question_type="multiple_choice"
        )
        self.client = Client()

    def test_poll_presentation(self):
        self.client.login(username = 'johndoe', password = 'Password123')

        response = self.client.get(reverse('poll_management:display_code', args=[self.poll.pk]))

        # check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # check that the correct template was used
        self.assertTemplateUsed(response, 'display_code.html')

        # check that the context contains the expected poll
        self.assertEqual(response.context['poll'], self.poll)


        # check that the context contains the expected questions
        self.assertIn(self.question, response.context['poll'].questions.all())


