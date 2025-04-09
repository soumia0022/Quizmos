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
    help = 'Seed responses for each question with better student distribution'

    def handle(self, *args, **kwargs):
        users = list(User.objects.filter(role="Student"))
        polls = list(Poll.objects.all())

        if not users or not polls:
            self.stdout.write(self.style.WARNING("No users or polls found."))
            return

        # Dictionary to track which poll IDs a student has already responded to
        student_poll_names = {user: set() for user in users}

        for poll in polls:
            questions = list(Question.objects.filter(poll=poll))
            if not questions:
                continue

            # Shuffle users so each run distributes responses differently
            random.shuffle(users)

            # Generate TWO session codes for each student per poll
            student_session_codes = {user: (random.randint(100000, 999999), random.randint(100000, 999999)) for user in users}

            # Each user can answer each poll name only once
            for user in users:
                if poll.title in student_poll_names[user]:
                    continue  # Skip this poll for this user

                # Mark this poll name as answered for this user
                student_poll_names[user].add(poll.title)

                # Count how many questions the user has answered
                student_response_count = 0
                max_responses = len(questions)

                for index, question in enumerate(questions):
                    if student_response_count >= max_responses:
                        break

                    # Alternate session codes
                    session_code = student_session_codes[user][index % 2]

                    response_data = {
                        'question': question,
                        'user': user,
                        'poll': poll,
                        'session_code': session_code,
                    }

                    # Determine response type
                    question_type = question.question_type
                    is_correct = False  # Default

                    if question_type == "multiple_choice":
                        options = question.multiple_choice_options or []
                        selected_options = random.sample(options, min(2, len(options))) if options else ["Option A", "Option B"]
                        response_data['selected_options'] = selected_options
                        is_correct = set(selected_options) == set(question.multiple_choice_answers or [])
                        response_type = MultipleChoiceResponse
                        response_data['is_correct'] = is_correct

                    elif question_type == "single_choice":
                        options = question.single_choice_option or []
                        selected_option = random.choice(options) if options else "Option A"
                        response_data['selected_option'] = selected_option
                        is_correct = selected_option in (question.single_choice_answers or [])
                        response_type = SingleChoiceResponse
                        response_data['is_correct'] = is_correct

                    elif question_type == "text_fill":
                        # Randomly decide whether to submit a correct or random answer
                        use_correct_answer = random.random() < 0.4  # ~40% chance of being correct
                        if use_correct_answer and question.text_fill_answer:
                            answer_text = question.text_fill_answer.strip()
                        else:
                            answer_text = random.choice(SAMPLE_TEXTS)
                        response_data['answer_text'] = answer_text
                        is_correct = answer_text.strip().lower() == (question.text_fill_answer or "").strip().lower()
                        response_type = TextFillResponse
                        response_data['is_correct'] = is_correct

                    elif question_type == "dropdown_fill":
                        options = question.get_dropdown_options()
                        selected_option = random.choice(options) if options else "Dropdown Option"
                        response_data['selected_option'] = selected_option
                        is_correct = selected_option.strip().lower() == (question.dropdown_correct_answer or "").strip().lower()
                        response_type = DropdownFillResponse
                        response_data['is_correct'] = is_correct

                    elif question_type == "match_question":
                        match_pairs = [{"left": opt, "right": ans} for opt, ans in zip(question.match_options, question.match_answers)]
                        response_data['match_responses'] = match_pairs
                        user_responses = [pair['right'] for pair in match_pairs]
                        is_correct = user_responses == (question.match_answers or [])
                        response_type = MatchQuestionResponse
                        response_data['is_correct'] = is_correct

                    elif question_type == "wordcloud":
                        words = random.sample(SAMPLE_WORDS, 2)
                        response_data['word_cloud_response'] = words
                        response_type = WordCloudResponse

                    elif question_type == "code_question":
                        code_lang = question.code_language.lower() if question.code_language else "python"
                        submitted_code = CODE_SNIPPETS.get(code_lang, CODE_SNIPPETS["python"])
                        response_data['submitted_code'] = submitted_code
                        response_type = CodeQuestionResponse

                    else:
                        continue  # Skip unsupported question types

                    # Create response instance
                    response_type.objects.create(**response_data)

                    # Increment response count for the user
                    student_response_count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully seeded responses for poll {poll.id}"))

