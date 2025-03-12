from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
    DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
    CodeQuestionResponse
)
import random
import json

User = get_user_model()

# Random text responses
SAMPLE_TEXTS = [
    "This is an interesting question!",
    "I believe the answer is quite complex.",
    "Not sure, but I would say something related to science.",
    "It depends on the context of the question.",
    "I need to think more about this."
]

# Random word cloud responses
SAMPLE_WORDS = ["innovation", "progress", "technology", "future", "creativity"]

# Code templates based on language
CODE_SNIPPETS = {
    "python": 'print("Hello World")',
    "javascript": 'console.log("Hello World")',
    "java": 'System.out.println("Hello World");'
}


class Command(BaseCommand):
    help = 'Seed responses for each question'

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())
        polls = list(Poll.objects.all())
        questions = list(Question.objects.all())

        for question in questions:
            responses = []
            session_code = None

            for i in range(10):
                user = random.choice(users)

                # Generate a new session code every 3 responses
                if i % 3 == 0:
                    session_code = random.randint(100000, 999999)

                response_data = {
                    'question': question,
                    'user': user,
                    'poll': question.poll,
                    'session_code': session_code,
                }

                # Determine response type based on question type
                question_type = question.question_type
                if question_type == "multiple_choice":
                    options = question.multiple_choice_options or []
                    selected_options = random.sample(options, min(2, len(options))) if options else ["Option A", "Option B"]
                    response_data['selected_options'] = json.dumps(selected_options)
                    response_type = MultipleChoiceResponse

                elif question_type == "single_choice":
                    options = question.single_choice_option or []
                    selected_option = random.choice(options) if options else "Option A"
                    response_data['selected_option'] = selected_option
                    response_type = SingleChoiceResponse

                elif question_type == "text_fill":
                    response_data['answer_text'] = random.choice(SAMPLE_TEXTS)
                    response_type = TextFillResponse

                elif question_type == "dropdown_fill":
                    options = question.get_dropdown_options()
                    selected_option = random.choice(options) if options else "Dropdown Option"
                    response_data['selected_option'] = selected_option
                    response_type = DropdownFillResponse

                elif question_type == "match_question":
                    match_pairs = {opt: ans for opt, ans in zip(question.match_options, question.match_answers)}
                    response_data['match_responses'] = json.dumps(match_pairs)
                    response_type = MatchQuestionResponse

                elif question_type == "wordcloud":
                    words = random.sample(SAMPLE_WORDS, 2)
                    response_data['word_cloud_response'] = json.dumps({words[0]: 3, words[1]: 5})
                    response_type = WordCloudResponse

                elif question_type == "code_question":
                    code_lang = question.code_language.lower() if question.code_language else "python"
                    submitted_code = CODE_SNIPPETS.get(code_lang, CODE_SNIPPETS["python"])
                    response_data['submitted_code'] = submitted_code
                    response_type = CodeQuestionResponse

                else:
                    continue  # Skip unsupported question types

                # Create the response instance
                response_type.objects.create(**response_data)

            self.stdout.write(self.style.SUCCESS(f'Successfully added 10 responses for question {question.id}'))
