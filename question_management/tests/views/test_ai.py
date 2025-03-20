from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse, Http404
import nltk
import random
import unittest
from django.contrib.auth.models import User
from django.test import Client, RequestFactory
from unittest.mock import patch, MagicMock
from question_management.views.add_question import add_question

from question_management.views.add_question import (
    extract_text_from_pdf,
    extract_text_from_docx,
    generate_questions_from_text,
    parse_generated_question,
    add_question
)


class AddQuestionTests(TestCase):

    @patch('pdfplumber.open')
    def test_extract_text_from_pdf(self, mock_open):
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Test content"
        mock_pdf.pages = [mock_page]
        mock_open.return_value.__enter__.return_value = mock_pdf
        result = extract_text_from_pdf(SimpleUploadedFile("test.pdf", b"content"))
        self.assertEqual(result, "Test content")

    @patch('pdfplumber.open')
    def test_extract_text_from_pdf_none(self, mock_open):
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = None
        mock_pdf.pages = [mock_page]
        mock_open.return_value.__enter__.return_value = mock_pdf
        result = extract_text_from_pdf(SimpleUploadedFile("test.pdf", b"content"))
        self.assertEqual(result, "")

    @patch('docx.Document')
    def test_extract_text_from_docx(self, mock_document):
        mock_doc = MagicMock()
        mock_para = MagicMock()
        mock_para.text = "Test paragraph"
        mock_doc.paragraphs = [mock_para]
        mock_document.return_value = mock_doc
        result = extract_text_from_docx(SimpleUploadedFile("test.docx", b"content"))
        self.assertEqual(result, "Test paragraph")

    @patch('nltk.sent_tokenize')
    @patch('random.sample')
    def test_generate_questions_from_text(self, mock_sample, mock_tokenize):
        mock_tokenize.return_value = ["Python is a programming language."]
        mock_sample.return_value = ["Java", "C++", "JavaScript"]
        result = generate_questions_from_text("Python is a programming language.")
        self.assertTrue(isinstance(result, list))
        if result:
            self.assertTrue("_____" in result[0]["question"])
            self.assertEqual(len(result[0]["options"]), 4)

    def test_generate_questions_from_text_empty(self):
        result = generate_questions_from_text("")
        self.assertEqual(result, [])

    @patch('nltk.sent_tokenize')
    @patch('random.sample')
    def test_generate_questions_uppercase(self, mock_sample, mock_tokenize):
        mock_tokenize.return_value = ["London is in England."]
        mock_sample.return_value = ["Paris", "Berlin", "Rome"]
        result = generate_questions_from_text("London is in England.")
        if result:
            self.assertEqual(len(result[0]["options"]), 4)
            self.assertTrue(result[0]["options"][0].startswith("A."))

    @patch('nltk.sent_tokenize')
    @patch('random.sample')
    def test_generate_questions_few_words(self, mock_sample, mock_tokenize):
        mock_tokenize.return_value = ["Code is fun."]
        mock_sample.side_effect = [["Code"], ["option", "choice", "alternative"]]
        result = generate_questions_from_text("Code is fun.")
        if result:
            self.assertEqual(len(result[0]["options"]), 4)

    def test_parse_generated_question(self):
        text = "What is Python?\nA. Language CORRECT\nB. Snake\nC. Game\nD. Food"
        result = parse_generated_question(text, "Python is a language.")
        self.assertEqual(result["question"], "What is Python?")
        self.assertEqual(result["answer"], "A. Language CORRECT")

    def test_parse_question_no_mark(self):
        text = "What is Python\nA. Language CORRECT\nB. Snake\nC. Game\nD. Food"
        result = parse_generated_question(text, "Python is a language.")
        self.assertEqual(result["question"], "What is Python?")

    def test_parse_question_missing_options(self):
        text = "What is Python?\nA. Language CORRECT"
        result = parse_generated_question(text, "Python is a language.")
        self.assertEqual(len(result["options"]), 4)

    def test_parse_question_answer_in_last(self):
        text = "What is Python?\nA. Language\nB. Snake\nC. Game\nD. Food\nCORRECT ANSWER: A"
        result = parse_generated_question(text, "Python is a language.")
        self.assertIsNotNone(result["answer"])
        self.assertIn(result["answer"], result["options"])

    def test_parse_question_error(self):
        with patch('builtins.print'):
            result = parse_generated_question("", None)
            self.assertIsNone(result)

    @patch('nltk.sent_tokenize')
    def test_empty_sentence_continue(self, mock_tokenize):
        mock_tokenize.return_value = ["", "This is a valid sentence with enough words."]
        with patch('random.sample', return_value=["distractor1", "distractor2", "distractor3"]):
            result = generate_questions_from_text("Sample text")
            self.assertTrue(isinstance(result, list))

    @patch('nltk.sent_tokenize')
    def test_uppercase_word_distractors(self, mock_tokenize):
        mock_tokenize.return_value = ["John is writing code."]
        with patch('random.sample', return_value=["Paris", "London", "Berlin"]):
            result = generate_questions_from_text("Sample text with proper noun")
            if result and len(result) > 0:
                options_text = ' '.join(result[0]["options"])
                self.assertTrue(any(city in options_text for city in ["Paris", "London", "Berlin"]))

    @patch('nltk.sent_tokenize')
    def test_lowercase_word_distractors(self, mock_tokenize):
        mock_tokenize.return_value = ["programming is fun and interesting."]
        with patch('random.sample', side_effect=[["code", "python", "java"], ["code", "python", "java"]]):
            result = generate_questions_from_text("Sample text with common words")
            if result and len(result) > 0:
                self.assertEqual(len(result[0]["options"]), 4)

    @patch('nltk.sent_tokenize')
    def test_not_enough_similar_words(self, mock_tokenize):
        mock_tokenize.return_value = ["This is a test."]
        def mock_set_func(words):
            return set()
        with patch('random.sample', return_value=["option", "choice", "alternative"]):
            with patch('builtins.set', side_effect=lambda x: set() if isinstance(x, list) else set(x)):
                result = generate_questions_from_text("Sample with no similar words")
                if result and len(result) > 0:
                    options_text = ' '.join(result[0]["options"])
                    self.assertTrue(any(word in options_text for word in ["option", "choice", "alternative"]))

    @patch('nltk.sent_tokenize')
    def test_adding_additional_options(self, mock_tokenize):
        mock_tokenize.return_value = ["This is another test."]
        original_sample = random.sample
        def mock_sample(*args, **kwargs):
            if args[0] == ["option", "choice", "alternative"]:
                return ["option"]
            return original_sample(*args, **kwargs)
        with patch('random.sample', side_effect=mock_sample):
            result = generate_questions_from_text("Sample text")
            if result and len(result) > 0:
                self.assertEqual(len(result[0]["options"]), 4)
                options_text = ' '.join(result[0]["options"])
                self.assertTrue("Additional" in options_text)

    @patch('nltk.sent_tokenize')
    def test_break_after_question_found(self, mock_tokenize):
        mock_tokenize.return_value = ["Python and Java are popular programming languages."]
        with patch('random.sample', return_value=["Ruby", "C++", "JavaScript"]):
            result = generate_questions_from_text("Sample text")
            if len(result) > 0:
                questions_per_sentence = {}
                for q in result:
                    sentence_base = q["question"].replace("_____", "").replace("?", "").strip()
                    if sentence_base in questions_per_sentence:
                        questions_per_sentence[sentence_base] += 1
                    else:
                        questions_per_sentence[sentence_base] = 1
                for sentence, count in questions_per_sentence.items():
                    self.assertEqual(count, 1, f"Found multiple questions for sentence: {sentence}")

    @patch('nltk.sent_tokenize')
    def test_fallback_distractor_options(self, mock_tokenize):
        mock_tokenize.return_value = ["This is a simple test."]
        with patch('random.sample', side_effect=lambda *args, **kwargs: []):
            result = generate_questions_from_text("Sample text")
            if result and len(result) > 0:
                options_text = ' '.join(result[0]["options"])
                fallback_options = ["option", "choice", "alternative"]
                self.assertTrue(any(opt in options_text for opt in fallback_options))

    class FileUploadTests(unittest.TestCase):

        def setUp(self):
            self.client = Client()

        def test_pdf_file_upload(self):
            pdf_content = b"%PDF-1.4 sample content"
            uploaded_file = SimpleUploadedFile("sample.pdf", pdf_content, content_type="application/pdf")
            response = self.client.post('/your-endpoint-url/', {'file': uploaded_file})
            self.assertEqual(response.status_code, 200)
            self.assertIn("questions", response.json())

        def test_docx_file_upload(self):
            docx_content = b"PK\x03\x04 sample docx content"
            uploaded_file = SimpleUploadedFile("sample.docx", docx_content,
                                               content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response = self.client.post('/your-endpoint-url/', {'file': uploaded_file})
            self.assertEqual(response.status_code, 200)
            self.assertIn("questions", response.json())

        def test_unsupported_file_format(self):
            txt_content = b"This is a plain text file."
            uploaded_file = SimpleUploadedFile("sample.txt", txt_content, content_type="text/plain")
            response = self.client.post('/your-endpoint-url/', {'file': uploaded_file})
            self.assertEqual(response.status_code, 200)
            self.assertIn("error", response.json())
            self.assertEqual(response.json()["error"], "Unsupported file format.")

        def test_empty_content_handling(self):
            empty_pdf_content = b""
            uploaded_file = SimpleUploadedFile("empty.pdf", empty_pdf_content, content_type="application/pdf")
            response = self.client.post('/your-endpoint-url/', {'file': uploaded_file})
            self.assertEqual(response.status_code, 200)
            self.assertIn("error", response.json())
            self.assertEqual(response.json()["error"], "No questions could be generated from the document.")

    if __name__ == "__main__":
        unittest.main()
