from django.test import TransactionTestCase
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import asyncio

from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
    MatchQuestionResponse, DropdownFillResponse, WordCloudResponse,
    CodeQuestionResponse
)
from user_management.models import User
from poll_management.consumers.poll_consumer_db import DatabaseHandler


class TestDatabaseHandler(TransactionTestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    async def asyncSetUp(self):
        # Set up users
        self.lecturer = await database_sync_to_async(User.objects.get)(username='johndoe')
        await database_sync_to_async(setattr)(self.lecturer, 'role', 'Lecturer')
        await database_sync_to_async(self.lecturer.save)()

        self.student = await database_sync_to_async(User.objects.get)(username='janedoe')
        await database_sync_to_async(setattr)(self.student, 'role', 'Student')
        await database_sync_to_async(self.student.save)()

        # Create poll
        self.poll = await database_sync_to_async(Poll.objects.create)(
            title="Test Poll",
            user=self.lecturer,
            number_code=123456
        )

        # Create questions
        self.mcq_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Multiple choice question?",
            question_type="multiple_choice",
            multiple_choice_options=['Option A', 'Option B', 'Option C'],
            multiple_choice_answers=['Option A', 'Option C']
        )

        self.scq_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Single choice question?",
            question_type="single_choice",
            single_choice_option=['Yes', 'No', 'Maybe'],
            single_choice_answers=['Yes']
        )

        self.text_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Text question?",
            question_type="text_fill",
            text_fill_answer="Test answer"
        )

        self.match_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Match question",
            question_type="match_question",
            match_options=['A', 'B', 'C'],
            match_answers=['1', '2', '3']
        )

        self.dropdown_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Dropdown question",
            question_type="dropdown_fill",
            dropdown_options="Red,Green,Blue",
            dropdown_correct_answer="Blue"
        )

        self.wordcloud_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Wordcloud question",
            question_type="wordcloud",
            wordcloud_question="Enter your word(s):"
        )

        self.code_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Code question",
            question_type="code_question",
            code_language="python",
            correct_code="print('Hello, World!')"
        )

        # Initialize database handler
        self.db_handler = DatabaseHandler()

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.asyncSetUp())



    def tearDown(self):
        # Close any pending Redis connections
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        if hasattr(channel_layer, 'connection_pool'):
            channel_layer.connection_pool.disconnect()

        self.loop.close()
        super().tearDown()

    async def test_get_question(self):
        """Test retrieving question details"""
        # Get MCQ question
        question = await self.db_handler.get_question(self.mcq_question.id)
        self.assertIsNotNone(question)
        self.assertEqual(question['id'], self.mcq_question.id)
        self.assertEqual(question['text'], "Multiple choice question?")
        self.assertEqual(question['type'], "multiple_choice")
        self.assertEqual(question['mcq_options'], ['Option A', 'Option B', 'Option C'])

        # Get dropdown question
        dropdown_question = await self.db_handler.get_question(self.dropdown_question.id)
        self.assertIsNotNone(dropdown_question)
        self.assertEqual(dropdown_question['dropdown_options'], ['Red', 'Green', 'Blue'])
        self.assertEqual(dropdown_question['dropdown_correct_answer'], 'Blue')

        # Get non-existent question
        question = await self.db_handler.get_question(99999)
        self.assertIsNone(question)

    async def test_get_all_questions(self):
        """Test retrieving all questions for a poll"""
        questions = await self.db_handler.get_all_questions(self.poll)
        self.assertEqual(len(questions), 7)  # We created 7 questions in setup

        # Check if all questions are returned
        question_ids = [q.id for q in questions]
        self.assertIn(self.mcq_question.id, question_ids)
        self.assertIn(self.scq_question.id, question_ids)
        self.assertIn(self.text_question.id, question_ids)
        self.assertIn(self.match_question.id, question_ids)
        self.assertIn(self.dropdown_question.id, question_ids)
        self.assertIn(self.wordcloud_question.id, question_ids)
        self.assertIn(self.code_question.id, question_ids)

    async def test_get_correct_answers(self):
        """Test retrieving correct answers for different question types"""
        # MCQ answers
        mcq_answers = await self.db_handler.get_correct_answers(self.mcq_question.id)
        self.assertEqual(mcq_answers, ['Option A', 'Option C'])

        # Single choice answers
        scq_answers = await self.db_handler.get_correct_answers(self.scq_question.id)
        self.assertEqual(scq_answers, ['Yes'])

        # Text fill answer
        text_answer = await self.db_handler.get_correct_answers(self.text_question.id)
        self.assertEqual(text_answer, 'Test answer')

        # Match answers
        match_answers = await self.db_handler.get_correct_answers(self.match_question.id)
        self.assertEqual(match_answers, ['1', '2', '3'])

        # Dropdown answer
        dropdown_answer = await self.db_handler.get_correct_answers(self.dropdown_question.id)
        self.assertEqual(dropdown_answer, 'Blue')

        # Wordcloud has no correct answer
        wordcloud_answer = await self.db_handler.get_correct_answers(self.wordcloud_question.id)
        self.assertIsNone(wordcloud_answer)

        # Code question answer
        code_answer = await self.db_handler.get_correct_answers(self.code_question.id)
        self.assertEqual(code_answer, "print('Hello, World!')")

        # Non-existent question
        non_existent = await self.db_handler.get_correct_answers(99999)
        self.assertIsNone(non_existent)


    async def test_save_response_invalid_type(self):
        """Test saving response with invalid type"""
        # Attempt to save response with invalid type
        success = await self.db_handler.save_response(
            self.student,
            self.poll,
            self.poll.number_code,
            self.mcq_question.id,
            'invalid_type',
            'Invalid data'
        )
        self.assertFalse(success)

    async def test_save_response_nonexistent_question(self):
        """Test saving response for non-existent question"""
        # Attempt to save response for non-existent question
        success = await self.db_handler.save_response(
            self.student,
            self.poll,
            self.poll.number_code,
            99999,
            'multiple_choice',
            ['Option A']
        )
        self.assertFalse(success)

    async def test_save_multiple_choice_partially_correct(self):
        """Test saving partially correct multiple choice response"""
        # (This should be marked as partially correct)
        response_data = ['Option A']  # one of the correct answers
        success = await self.db_handler.save_response(
            self.student,
            self.poll,
            self.poll.number_code,
            self.mcq_question.id,
            'multiple_choice',
            response_data
        )

        self.assertTrue(success)

        queryset = await database_sync_to_async(lambda: MultipleChoiceResponse.objects.filter(
            user=self.student,
            question=self.mcq_question
        ))()

        response = await database_sync_to_async(lambda: queryset.first())()

        self.assertIsNotNone(response)
        self.assertEqual(response.selected_options, response_data)
        self.assertFalse(response.is_correct)  # not fully correct
        self.assertTrue(response.is_partially_correct)  #  partially correct

        # (Should not be marked as partially correct)
        response_data = ['Option A', 'Option B']  # Option B is not a correct answer
        success = await self.db_handler.save_response(
            self.student,
            self.poll,
            self.poll.number_code,
            self.mcq_question.id,
            'multiple_choice',
            response_data
        )

        self.assertTrue(success)


        queryset = await database_sync_to_async(lambda: MultipleChoiceResponse.objects.filter(
            user=self.student,
            question=self.mcq_question
        ))()

        response = await database_sync_to_async(lambda: queryset.first())()

        self.assertIsNotNone(response)
        self.assertEqual(response.selected_options, response_data)
        self.assertFalse(response.is_correct)
        self.assertFalse(response.is_partially_correct)  # not partially correct due to wrong selections

    async def test_save_match_question_partially_correct(self):
        """Test saving partially correct match question responses in both formats"""

        match_response_data = {
            'A': '1',  # correct match
            'B': '1',  # incorrect match (should be '2')
            'C': '1'  # incorrect match (should be '3')
        }

        success = await self.db_handler.save_response(
            self.student,
            self.poll,
            self.poll.number_code,
            self.match_question.id,
            'match_question',
            match_response_data
        )

        self.assertTrue(success)

        queryset = await database_sync_to_async(lambda: MatchQuestionResponse.objects.filter(
            user=self.student,
            question=self.match_question
        ))()

        response = await database_sync_to_async(lambda: queryset.first())()

        self.assertIsNotNone(response)
        self.assertEqual(response.match_responses, match_response_data)
        self.assertFalse(response.is_correct)  # not fully correct
        self.assertTrue(response.is_partially_correct)  #  partially correct


        match_response_data_list = [
            {'left': 'A', 'right': '1'},  # correct
            {'left': 'B', 'right': '1'},  # incorrect (should be '2')
            {'left': 'C', 'right': '1'}  # incorrect (should be '3')
        ]

        success = await self.db_handler.save_response(
            self.student,
            self.poll,
            self.poll.number_code,
            self.match_question.id,
            'match_question',
            match_response_data_list
        )

        self.assertTrue(success)

        queryset = await database_sync_to_async(lambda: MatchQuestionResponse.objects.filter(
            user=self.student,
            question=self.match_question
        ))()

        response = await database_sync_to_async(lambda: queryset.last())()

        self.assertIsNotNone(response)
        self.assertEqual(response.match_responses, match_response_data_list)
        self.assertFalse(response.is_correct)  # not fully correct
        self.assertTrue(response.is_partially_correct)  #  partially correct

        # no correct matches (should not be partially correct)
        all_wrong_response = [
            {'left': 'A', 'right': '2'},  # incorrect
            {'left': 'B', 'right': '3'},  # incorrect
            {'left': 'C', 'right': '1'}  # incorrect
        ]

        success = await self.db_handler.save_response(
            self.student,
            self.poll,
            self.poll.number_code,
            self.match_question.id,
            'match_question',
            all_wrong_response
        )

        self.assertTrue(success)

        queryset = await database_sync_to_async(lambda: MatchQuestionResponse.objects.filter(
            user=self.student,
            question=self.match_question
        ))()

        response = await database_sync_to_async(lambda: queryset.last())()

        self.assertIsNotNone(response)
        self.assertFalse(response.is_correct)
        self.assertFalse(response.is_partially_correct)  # not partially correct since no matches are correct