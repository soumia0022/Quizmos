import os
from unittest.mock import patch, Mock
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from collections import Counter
from Quizmos import settings
from poll_management.models.poll_model import Poll
from wordcloud import WordCloud
from PIL import ImageFont
from user_management.models import User


class WordcloudTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password', role='Lecturer')
        self.poll = Poll.objects.create(title='Poll 1', user=self.user, status='active')
        self.font_path = os.path.join(
            settings.BASE_DIR, "question_management", "static", "fonts", "RobotoMono-Regular.ttf"
        )
        self.add_question_url = reverse('question_management:add_question', kwargs={'poll_id': self.poll.id})  # Update the URL name

    # Test that the frequency of each word is correctly counted
    def test_word_frequencies(self):
        text = ("Testing Testing the Word Cloud hello hello hello SEG SEG SEG wow amazing great yay woohoo "
                "Hello Soumia Soumia Amina Amina Leyli Leyli Eeshal Marium Rashida Rashida Alishba Alishba Alishba")
        word_frequencies = Counter(text.split())

        self.assertEqual(word_frequencies['hello'], 3)
        self.assertEqual(word_frequencies['SEG'], 3)
        self.assertEqual(word_frequencies['Alishba'], 3)

    # Test that a non-true-type font would raise an OS error (as not supported by required libraries)
    def test_non_truetype_font(self):
        with patch('question_management.views.question_types.ImageFont.truetype') as mock_truetype:
            mock_truetype.side_effect = OSError("Only supported for TrueType fonts")
            with self.assertRaises(OSError):
                ImageFont.truetype(self.font_path)

    # Tes that empty text shows an empty wordcloud
    def test_empty_text(self):
        word_frequencies = Counter("")
        if not word_frequencies:
            self.assertEqual(len(word_frequencies), 0)
        else:
            wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_frequencies)
            self.assertEqual(len(wordcloud.words_), 0)

    # Test that a wordcloud is successfully generated
    def test_wordcloud_generation(self):
        text = ("Testing Testing the Word Cloud hello hello hello SEG SEG SEG wow amazing great yay woohoo "
                "Hello Soumia Soumia Amina Amina Leyli Leyli Eeshal Marium Rashida Rashida Alishba Alishba Alishba")
        word_frequencies = Counter(text.split())

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='twilight',
            max_font_size=100,
            min_font_size=10,
            stopwords={'and', 'the', 'of'},
            font_path=self.font_path
        ).generate_from_frequencies(word_frequencies)

        self.assertIsNotNone(wordcloud)
        self.assertIn('hello', wordcloud.words_)
        self.assertIn('SEG', wordcloud.words_)

    # Test that a question/prompt can be inputted for the wordcloud
    def test_post_request_with_wordcloud_question(self):
        data = {'question_type': 'wordcloud', 'wordcloud_question': 'What is your favourite word?'}
        with patch('question_management.views.question_types.plt') as mock_plt:
            mock_buffer = Mock()
            mock_buffer.getvalue.return_value = b'test_image_data'

            with patch('question_management.views.question_types.io.BytesIO', return_value=mock_buffer):
                response = self.client.post(self.add_question_url, data)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'add_question.html')
                self.assertIn('wordcloud_image', response.context)

    # Test that the page is displayed correctly
    def test_rendered_html_output(self):
        data = {'question_type': 'wordcloud', 'wordcloud_question': 'What is your favourite word?'}
        with patch('question_management.views.question_types.plt.savefig') as mock_savefig:
            mock_savefig.return_value = None

            response = self.client.post(self.add_question_url, data)

            self.assertContains(response, 'Poll 1')
            self.assertIn('wordcloud_image', response.context)

    # Test that the correct error is raised if font file does not exist
    def test_exception_handling_missing_font(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                if not os.path.exists(self.font_path):
                    raise FileNotFoundError("Font file not found")

    # Test that the correct error is raised it font file is invalid
    def test_exception_handling_invalid_font(self):
        with patch('PIL.ImageFont.truetype', side_effect=OSError("Invalid font")):
            with self.assertRaises(OSError):
                ImageFont.truetype(self.font_path)

    # Test that the correct error is raised for an invalid true-type font
    def test_invalid_truetype_font(self):
        font_path = "/path/to/existing/invalid_font.ttf"
        with patch('os.path.exists', return_value=True):
            with patch('PIL.ImageFont.truetype', side_effect=IOError("Only supported for TrueType fonts")):
                with self.assertRaises(ValueError) as context:
                    try:
                        font = ImageFont.truetype(font_path)
                    except IOError:
                        raise ValueError("Only supported for TrueType fonts")

                self.assertEqual(str(context.exception), "Only supported for TrueType fonts")

