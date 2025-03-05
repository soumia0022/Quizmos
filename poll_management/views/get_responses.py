from response_management.models.response_model import DropdownFillResponse, MultipleChoiceResponse, \
    SingleChoiceResponse, TextFillResponse, MatchQuestionResponse
from question_management.models.question_models import Question

from django.http import JsonResponse
import json
from typing import Dict, List, Union


class QuestionResponseCounter:
    def __init__(self, question: Question):
        self.question = question
        self.question_type = question.question_type
        self.response_handlers = {
            'multiple_choice': self._get_mcq_responses,
            'single_choice': self._get_scq_responses,
            'dropdown_fill': self._get_dropdown_responses,
            'text_fill' : self._get_text_responses,
            'match_question' : self._get_match_responses,
        }

    def get_counts(self) -> JsonResponse:
        """Get response counts for the question."""
        try:
            if self.question_type not in self.response_handlers:
                return JsonResponse({
                    'error': f'Unsupported question type: {self.question_type}'
                }, status=400)

            counts_dict = self.response_handlers[self.question_type]()

            if self.question_type == 'text_fill':
                return JsonResponse(counts_dict)
            if self.question_type == 'match_question':
                total_responses = MatchQuestionResponse.objects.filter(
                    question=self.question
                ).count()

                return JsonResponse({
                    'question_id': self.question.id,
                    'question_type': self.question_type,
                    'counts': counts_dict,
                    'total_responses': total_responses
                })

            return JsonResponse({
                'question_id': self.question.id,
                'question_type': self.question_type,
                'counts': counts_dict
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error processing responses: {str(e)}'
            }, status=500)

    def _get_mcq_responses(self) -> Dict[int, int]:
        """Handle multiple choice question responses."""
        options = list(self.question.multiple_choice_options)
        counts_dict = {i: 0 for i in range(len(options))}
        responses = MultipleChoiceResponse.objects.filter(
            question=self.question, session_code=self.question.poll.number_code
        ).values_list('selected_options', flat=True)

        for selected_values in responses:
            self._process_mcq_response(selected_values, options, counts_dict)

        return counts_dict

    def _process_mcq_response(self, selected_values: Union[str, List],
                              options: List[str], counts_dict: Dict[int, int]) -> None:
        """Process individual MCQ response."""
        if isinstance(selected_values, str):
            selected_values = json.loads(selected_values)

        for selected_value in selected_values:
            if selected_value in options:
                selected_index = options.index(selected_value)
                counts_dict[selected_index] += 1

    def _get_scq_responses(self) -> Dict[int, int]:
        """Handle single choice question responses."""
        options = list(self.question.single_choice_option)
        counts_dict = {i: 0 for i in range(len(options))}
        responses = SingleChoiceResponse.objects.filter(
            question=self.question, session_code=self.question.poll.number_code
        ).values_list('selected_option', flat=True)

        for selected_value in responses:
            self._process_scq_response(selected_value, options, counts_dict)

        return counts_dict

    def _process_scq_response(self, selected_value: str,
                              options: List[str], counts_dict: Dict[int, int]) -> None:
        """Process individual SCQ response."""
        cleaned = str(selected_value).strip()
        if cleaned in options:
            selected_index = options.index(cleaned)
            counts_dict[selected_index] += 1

    def _get_dropdown_responses(self) -> Dict[int, int]:
        """Handle dropdown question responses."""
        options = [opt.strip() for opt in self.question.dropdown_options.split(',')]
        counts_dict = {i: 0 for i in range(len(options))}
        responses = DropdownFillResponse.objects.filter(
            question=self.question, session_code=self.question.poll.number_code
        ).values_list('selected_option', flat=True)

        for selected_value in responses:
            self._process_scq_response(selected_value, options, counts_dict)

        return counts_dict

    def _get_text_responses(self) -> Dict[str, List[str]]:
        """Handle text fill responses."""
        responses = TextFillResponse.objects.filter(
            question=self.question, session_code=self.question.poll.number_code
        ).values_list('answer_text', flat=True)

        # Convert QuerySet to list and filter out empty responses
        response_list = [resp.strip() for resp in responses if resp and resp.strip()]

        return {
            'question_id': self.question.id,
            'question_type': 'text_fill',
            'responses': response_list
        }

    def _get_match_responses(self) -> Dict:
        """
        Handle match question responses.
        """
        responses = MatchQuestionResponse.objects.filter( question=self.question, session_code=self.question.poll.number_code).values_list('match_responses', flat=True)

        options = self.question.match_options

        # make an empty dictionary in this format: {option: {possible_match: count}}
        counts = {option: {ans: 0 for ans in self.question.match_answers} for option in options}

        for response_set in responses:

            for match in response_set:
                if isinstance(match, dict) and 'left' in match and 'right' in match:
                    left_option = match['left']
                    right_match = match['right']
                    if left_option in counts and right_match in counts[left_option]:
                        counts[left_option][right_match] += 1

        return counts


def get_question_response_counts(request, poll_code, question_id):
    question = Question.objects.filter(id=question_id).first()
    if not question:
        return JsonResponse({
            'error': f'Question {question_id} not found'
        }, status=404)

    counter = QuestionResponseCounter(question)
    return counter.get_counts()
