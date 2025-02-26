from django.test import SimpleTestCase
from poll_management.helpers import format_youtube_link
class FormatYouTubeLinkTest(SimpleTestCase):

    def test_format_youtube_link(self):
        youtube_urls = [
            ("https://youtu.be/dQw4w9WgXcQ", "https://www.youtube.com/embed/dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/embed/dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "https://www.youtube.com/embed/dQw4w9WgXcQ"),
            ("https://youtube.com/v/dQw4w9WgXcQ", "https://www.youtube.com/embed/dQw4w9WgXcQ"),
        ]

        for original_url, expected_url in youtube_urls:
            self.assertEqual(format_youtube_link(original_url), expected_url)


