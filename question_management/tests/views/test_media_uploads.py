from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class QuestionFileUploadTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', role='Lecturer')
        self.client.login(username='testuser', password='password')

        self.poll = Poll.objects.create(
            title="Sample Poll",
            user=self.user,
        )

    def test_add_question_with_audio_and_video_files(self):
        self.client.login(username='lecturer', password='password')

        # Create mock audio and video files
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

        response = self.client.post(reverse('question_management:add_question', args=[self.poll.id]), {
            'question_type': 'text_fill',
            'text_fill_question': 'What is an apple?',
            'text_fill_answer': 'a fruit',
            'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'audio_file': audio_file,
            'video_file': video_file
        })

        self.assertEqual(response.status_code, 302)  # Ensure redirect happens
        questions = Question.objects.filter(poll_id=self.poll.id)
        self.assertEqual(len(questions), 1)

        question = questions[0]
        self.assertEqual(question.text_fill_question, 'What is an apple?')
        self.assertEqual(question.text_fill_answer, 'a fruit')
        self.assertEqual(question.youtube_link, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.assertIsNotNone(question.audio_file)
        self.assertIsNotNone(question.video_file)

    def test_add_dropdown_fill_question_with_audio_and_video_files(self):
        self.client.login(username='lecturer', password='password')

        # Create mock audio and video files
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

        response = self.client.post(reverse('question_management:add_question', args=[self.poll.id]), {
            'question_type': 'dropdown_fill',
            'dropdown_fill_question': 'What is an apple?',
            'dropdown_correct_answer': 'a fruit',
            'additional_options': ['a vegetable', 'a snack'],
            'audio_file': audio_file,
            'video_file': video_file
        })

        self.assertEqual(response.status_code, 302)  # Ensure redirect happens
        questions = Question.objects.filter(poll_id=self.poll.id)
        self.assertEqual(len(questions), 1)

        question = questions[0]
        self.assertEqual(question.dropdown_fill_question, 'What is an apple?')
        self.assertEqual(question.dropdown_options, 'a fruit,a vegetable,a snack')
        self.assertIsNotNone(question.audio_file)
        self.assertIsNotNone(question.video_file)

    def test_add_multiple_choice_question_with_audio_and_video_files(self):
        self.client.login(username='lecturer', password='password')

        # Create mock audio and video files
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

        response = self.client.post(reverse('question_management:add_question', args=[self.poll.id]), {
            'question_type': 'multiple_choice',
            'multiple_choice_question': 'What is an apple?',
            'multiple_choice_options[]': ['a fruit', 'a vegetable', 'a snack'],
            'multiple_choice_answers[]': ['a fruit'],
            'audio_file': audio_file,
            'video_file': video_file
        })

        self.assertEqual(response.status_code, 302)  # Ensure redirect happens
        questions = Question.objects.filter(poll_id=self.poll.id)
        self.assertEqual(len(questions), 1)

        question = questions[0]
        self.assertEqual(question.multiple_choice_question, 'What is an apple?')
        self.assertEqual(question.multiple_choice_options, ['a fruit', 'a vegetable', 'a snack'])
        self.assertEqual(question.multiple_choice_answers, ['a fruit'])
        self.assertIsNotNone(question.audio_file)
        self.assertIsNotNone(question.video_file)

    def test_add_single_choice_question_with_audio_and_video_files(self):
        self.client.login(username='lecturer', password='password')

        # Create mock audio and video files
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

        response = self.client.post(reverse('question_management:add_question', args=[self.poll.id]), {
            'question_type': 'single_choice',
            'single_choice_question': 'What is an apple?',
            'single_choice_options[]': ['a fruit'],
            'single_choice_answers[]': ['a fruit'],
            'audio_file': audio_file,
            'video_file': video_file
        })

        self.assertEqual(response.status_code, 302)  # Ensure redirect happens
        questions = Question.objects.filter(poll_id=self.poll.id)
        self.assertEqual(len(questions), 1)

        question = questions[0]
        self.assertEqual(question.single_choice_question, 'What is an apple?')
        self.assertEqual(question.single_choice_option, ['a fruit'])
        self.assertEqual(question.single_choice_answers, 'a fruit')
        self.assertIsNotNone(question.audio_file)
        self.assertIsNotNone(question.video_file)

    def test_add_wordcloud_question_with_audio_and_video_files(self):
        self.client.login(username='lecturer', password='password')

        # Create mock audio and video files
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

        response = self.client.post(reverse('question_management:add_question', args=[self.poll.id]), {
            'question_type': 'wordcloud',
            'wordcloud_question': 'Describe the features of an apple',
            'audio_file': audio_file,
            'video_file': video_file
        })

        questions = Question.objects.filter(poll_id=self.poll.id)
        self.assertEqual(len(questions), 1)

        question = questions[0]
        self.assertEqual(question.wordcloud_question, 'Describe the features of an apple')
        self.assertIsNotNone(question.audio_file)
        self.assertIsNotNone(question.video_file)

    def test_add_match_question_with_audio_and_video_files(self):
        self.client.login(username='lecturer', password='password')

        # Create mock audio and video files
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

        response = self.client.post(reverse('question_management:add_question', args=[self.poll.id]), {
            'question_type': 'match_question',
            'match_question': 'Match the following items',
            'match_question_options[]': ['Apple', 'Banana', 'Carrot'],
            'match_question_answers[]': ['Fruit', 'Fruit', 'Vegetable'],
            'audio_file': audio_file,
            'video_file': video_file
        })

        self.assertEqual(response.status_code, 302)  # Ensure redirect happens
        questions = Question.objects.filter(poll_id=self.poll.id)
        self.assertEqual(len(questions), 1)

        question = questions[0]
        self.assertEqual(question.match_question, 'Match the following items')
        self.assertEqual(question.match_options, ['Apple', 'Banana', 'Carrot'])
        self.assertEqual(question.match_answers, ['Fruit', 'Fruit', 'Vegetable'])
        self.assertIsNotNone(question.audio_file)
        self.assertIsNotNone(question.video_file)


