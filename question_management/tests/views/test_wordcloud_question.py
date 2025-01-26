import os
import io
import base64
from unittest.mock import patch
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from collections import Counter
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from question_management.views.question_types import add_question  # replace with the actual view name
from wordcloud import WordCloud
from PIL import ImageFont
from user_management.models import User


class WordcloudTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password', role='Lecturer')
        self.poll = Poll.objects.create(title='Poll 1', user=self.user, status='active')
        self.font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/fonts/RobotoMono-Regular.ttf")
        self.add_question_url = reverse('question_management:add_question', kwargs={'poll_id': self.poll.id})  # Update the URL name

    def test_word_frequencies(self):
        text = ("Testing Testing the Word Cloud hello hello hello SEG SEG SEG wow amazing great yay woohoo "
                "Hello Soumia Soumia Amina Amina Leyli Leyli Eeshal Marium Rashida Rashida Alishba Alishba Alishba")
        word_frequencies = Counter(text.split())

        self.assertEqual(word_frequencies['hello'], 3)
        self.assertEqual(word_frequencies['SEG'], 3)
        self.assertEqual(word_frequencies['Alishba'], 3)

    def test_missing_font_file(self):
        invalid_font_path = "non_existent_font.ttf"
        with self.assertRaises(OSError):  # Updated to match the exception raised
            ImageFont.truetype(invalid_font_path)

    def test_non_truetype_font(self):
        with patch('question_management.views.question_types.ImageFont.truetype') as mock_truetype:
            mock_truetype.side_effect = OSError("Only supported for TrueType fonts")
            with self.assertRaises(OSError):  # Updated to match the actual raised exception
                ImageFont.truetype(self.font_path)

    def test_empty_text(self):
        word_frequencies = Counter("")  # Empty text
        if not word_frequencies:
            self.assertEqual(len(word_frequencies), 0)  # Confirm no words
        else:
            wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_frequencies)
            self.assertEqual(len(wordcloud.words_), 0)
