from channels.db import database_sync_to_async
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from response_management.models.response_model import (
    MatchQuestionResponse, MultipleChoiceResponse,
    SingleChoiceResponse, DropdownFillResponse, TextFillResponse,
    WordCloudResponse, CodeQuestionResponse
)


class DatabaseHandler:
    """Handles all database operations for the poll consumer."""

    @staticmethod
    @database_sync_to_async
    def get_poll(poll_code):
        """Get poll details from database."""
        try:
            return Poll.objects.get(number_code=poll_code)
        except Poll.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def get_question(question_id):
        """Get question details from database."""
        try:
            question = Question.objects.get(id=question_id)
            dropdown_options = question.dropdown_options.split(',') if question.dropdown_options else []

            return {
                'id': question.id,
                'text': question.question_text,
                'type': question.question_type,
                'mcq_options': question.multiple_choice_options,
                'single_option': question.single_choice_option,
                'dropdown_options': dropdown_options,
                'match_options': question.match_options,
                'match_answers': question.match_answers,
                'wordcloud_question': question.wordcloud_question,
                'dropdown_correct_answer': question.dropdown_correct_answer,
                'code_language': question.code_language,
                'correct_code': question.correct_code,
                'question_timer': question.question_timer,
            }
        except Question.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def get_all_questions(poll):
        """Get all questions for current poll."""
        return list(Question.objects.filter(poll=poll))

    @staticmethod
    @database_sync_to_async
    def get_correct_answers(question_id):
        """Get correct answers for a question."""
        try:
            question = Question.objects.get(id=question_id)

            # Map question types to their answer fields
            type_to_answer = {
                'multiple_choice': question.multiple_choice_answers or [],
                'single_choice': question.single_choice_answers or [],
                'dropdown_fill': question.dropdown_correct_answer or "",
                'text_fill': question.text_fill_answer or "",
                'wordcloud': None,  # No correct answer for wordcloud
                'match_question': question.match_answers or [],
                'code_question': question.correct_code or ""
            }

            return type_to_answer.get(question.question_type)

        except Question.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def save_response(user, poll, session_code, question_id, response_type, response_data):
        """Save a user response."""
        try:
            question = Question.objects.get(id=question_id)

            # Map response types to models and field names
            response_models = {
                'match_question': (MatchQuestionResponse, 'match_responses'),
                'multiple_choice': (MultipleChoiceResponse, 'selected_options'),
                'single_choice': (SingleChoiceResponse, 'selected_option'),
                'dropdown_fill': (DropdownFillResponse, 'selected_option'),
                'text_fill': (TextFillResponse, 'answer_text'),
                'wordcloud': (WordCloudResponse, 'word_cloud_response'),
                'code_question': (CodeQuestionResponse, 'submitted_code'),
            }

            if response_type not in response_models:
                return False

            ResponseModel, field_name = response_models[response_type]

            # Determine correctness
            is_correct = False
            if response_type == 'multiple_choice':
                is_correct = set(response_data) == set(question.multiple_choice_answers or [])
            elif response_type == 'single_choice':
                is_correct = response_data in (question.single_choice_answers or [])
            elif response_type == 'dropdown_fill':
                is_correct = response_data.strip().lower() == (question.dropdown_correct_answer or "").strip().lower()
            elif response_type == 'text_fill':
                is_correct = response_data.strip().lower() == (question.text_fill_answer or "").strip().lower()
            elif response_type == 'match_question':
                # Process match questions based on input format
                match_options = question.match_options or []
                match_answers = question.match_answers or []

                if isinstance(response_data, dict):
                    # Format from test: {'A': '1', 'B': '2', 'C': '3'}
                    # Using index
                    is_correct = True
                    for i, option in enumerate(match_options):
                        if i >= len(match_answers) or option not in response_data or response_data[option] != \
                                match_answers[i]:
                            is_correct = False
                            break
                else:
                    # Handle the case where response_data might be a list
                    # This is for backward compatibility with any existing code
                    try:
                        if isinstance(response_data, list):
                            # Pairs like [{'left': 'A', 'right': '1'}, ...]
                            if all(isinstance(item, dict) for item in response_data):
                                # Try to extract responses from each format
                                if 'right' in response_data[0]:
                                    user_answers = [item['right'] for item in response_data]
                                    is_correct = user_answers == match_answers
                                elif 'left' in response_data[0] and 'right' in response_data[0]:
                                    # Build a dictionary from the list of pairs
                                    response_dict = {item['left']: item['right'] for item in response_data}
                                    is_correct = True
                                    for i, option in enumerate(match_options):
                                        if i >= len(match_answers) or option not in response_dict or response_dict[
                                            option] != match_answers[i]:
                                            is_correct = False
                                            break
                    except (IndexError, KeyError, TypeError):
                        is_correct = False

            # Prepare response data
            response_data_dict = {
                'user': user,
                'poll': poll,
                'question': question,
                'session_code': session_code,
                field_name: response_data,
                'is_correct': is_correct
            }

            # Check if response already exists
            existing_response = ResponseModel.objects.filter(
                user=user,
                poll=poll,
                session_code=session_code,
                question=question
            ).first()

            if existing_response:
                # Update existing response
                setattr(existing_response, field_name, response_data_dict[field_name])
                existing_response.is_correct = is_correct
                existing_response.save()
            else:
                # Create new response
                ResponseModel.objects.create(**response_data_dict)

            return True

        except Exception as e:
            return False