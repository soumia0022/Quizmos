from django.http import JsonResponse

class QuestionManager:
    """Class-based view to handle the validation of different types of questions when editing.

     The QuestionManager class is responsible for ensuring that once a question is edited, it still adheres to its
     validation constraints. The functions of this class are all static.
     """

    @staticmethod
    def validate_multiple_choice(question):
        """Validate multiple choice question."""
        if not question.multiple_choice_options:
            return JsonResponse({'error': 'At least one option is required for a multiple-choice question.'}, status=400)
        if not question.multiple_choice_answers:
            return JsonResponse({'error': 'At least one answer is required for a multiple-choice question.'}, status=400)
        return None

    @staticmethod
    def validate_single_choice(question):
        """Validate single choice question."""
        if not question.single_choice_answers or question.single_choice_answers == ['']:
            return JsonResponse({'error': 'At least one answer is required for a single-choice question.'}, status=400)
        if not question.single_choice_option or question.single_choice_option == ['']:
            return JsonResponse({'error': 'At least one option is required for a single-choice question.'}, status=400)
        if len(question.single_choice_answers) > 1:
            return JsonResponse({'error': 'Only one answer is allowed for a single-choice question.'}, status=400)
        return None

    @staticmethod
    def validate_text_fill(question):
        """Validate text fill question."""
        if not question.text_fill_question:
            return JsonResponse({'error': 'Question text is required'}, status=400)
        if not question.text_fill_answer:
            return JsonResponse({'error': 'Text fill answer is required'}, status=400)
        return None

    @staticmethod
    def validate_dropdown_fill(question):
        """Validate dropdown fill question."""
        if not question.dropdown_options:
            return JsonResponse({'error': 'At least one option is required for a dropdown-fill question.'}, status=400)
        if not question.dropdown_correct_answer:
            return JsonResponse({'error': 'A correct answer is required for a dropdown-fill question.'}, status=400)
        return None

    @staticmethod
    def validate_wordcloud(question):
        """Validate wordcloud question."""
        if not question.wordcloud_question:
            return JsonResponse({'error': 'Question text is required for a wordcloud question.'}, status=400)
        return None

    @staticmethod
    def validate_match_question(question):
        """Validate match question."""
        if not question.match_options:
            return JsonResponse({'error': 'At least one option is required for a match question.'}, status=400)
        if not question.match_answers:
            return JsonResponse({'error': 'At least one answer is required for a match question.'}, status=400)
        if len(question.match_options) != len(question.match_answers):
            return JsonResponse({'error': 'The number of options must match the number of answers.'}, status=400)
        return None
