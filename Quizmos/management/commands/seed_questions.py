from django.core.management.base import BaseCommand
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from faker import Faker
import random

class Command(BaseCommand):
    """Build automation command to seed questions in the database"""

    QUESTION_PER_POLL = 10
    help = 'Seed the database with questions'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_questions()

    def create_questions(self):
        """Generate questions for each poll"""
        polls = Poll.objects.all()
        if not polls.exists():
            print("No polls found. Please seed polls first.")
            return

        for poll in polls:
            self.seed_questions_for_poll(poll)
            print(f"Seeded {self.QUESTION_PER_POLL} questions for poll '{poll.title}'")

    def seed_questions_for_poll(self, poll):
        """Generate 10 questions per poll, one for each type"""
        question_types = [
            'dropdown_fill',
            'text_fill',
            'multiple_choice',
            'single_choice',
            'wordcloud',
            'match_question',
            'code_question'
        ]

        for question_type in question_types:
            self.generate_question(poll, question_type)

        # Add three additional questions of random types to make it 10
        for _ in range(3):
            random_type = random.choice(question_types)
            self.generate_question(poll, random_type)

    def generate_question(self, poll, question_type):
        """Generate a question with realistic data based on type"""
        question_data = {
            'poll': poll,
            'question_type': question_type,
            'timer': random.choice([None, 30, 60, 120]),
        }

        if question_type == 'dropdown_fill':
            question_text = self.faker.sentence()
            words = question_text.split()  # Split sentence into words

            if len(words) > 1:  # Ensure there are enough words to replace one
                correct_word = random.choice(words)  # Pick a random word from the sentence
                question_text_with_blank = question_text.replace(correct_word, "____",
                                                                 1)  # Replace only first occurrence
            else:
                correct_word = words[0]  # Fallback in case of a single-word sentence
                question_text_with_blank = "____"

            # Generate distractor options including the correct answer
            options = list(set(self.faker.words(3) + [correct_word]))  # Ensure correct word is in options
            random.shuffle(options)  # Shuffle so correct answer isn't always first

            question_data.update({
                'question_text': question_text_with_blank,
                'dropdown_fill_question': question_text_with_blank,
                'dropdown_options': ', '.join(options),
                'dropdown_correct_answer': correct_word,
            })

        elif question_type == 'text_fill':
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'text_fill_question': question_text,
                'text_fill_answer': self.faker.word(),
            })

        elif question_type == 'multiple_choice':
            options = self.faker.words(4)
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'multiple_choice_question': question_text,
                'multiple_choice_options': options,
                'multiple_choice_answers': random.sample(options, k=random.randint(1, 2)),
            })

        elif question_type == 'single_choice':
            options = self.faker.words(4)
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'single_choice_question': question_text,
                'single_choice_option': options,
                'single_choice_answers': [random.choice(options)],
            })

        elif question_type == 'wordcloud':
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'wordcloud_question': question_text,
            })

        elif question_type == 'match_question':
            options = self.faker.words(4)
            answers = self.faker.words(4)
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'match_question': question_text,
                'match_options': options,
                'match_answers': answers,
            })

        elif question_type == 'code_question':
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'code_question_text':question_text,
                'code_language': random.choice(["python", "javascript", "java"]),
                'code_test_cases': [{"input": "1 2", "output": "3"}, {"input": "3 3", "output": "6"}],
            })

        # Create question in the database
        Question.objects.create(**question_data)
