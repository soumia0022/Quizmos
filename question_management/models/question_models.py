from django.db import models
from poll_management.models.poll_model import Poll

# General info abt poll questions
class Question(models.Model):
    QUESTION_TYPES = [
        ('dropdown_fill', 'Dropdown Fill in the Blank'), # database name, display name
        ('text_fill', 'Text Fill in the Blank'),
        ('multiple_choice', 'Multiple Choice'),
        ('single_choice', 'Single Choice'),
    ]
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE, default=1) # question associated w poll
                                        # related name questions to allow you to do something like poll.questions.all() to get
                                        # all qs for that poll
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')

    # Fields for different question types
    text_fill_question = models.TextField(null=True, blank=True)
    text_fill_answer = models.TextField(null=True, blank=True)
    dropdown_fill_question = models.TextField(null=True, blank=True)
    dropdown_options = models.TextField(null=True, blank=True)  # comma-separated options for dropdown
    multiple_choice_question = models.TextField(null=True, blank=True)
    multiple_choice_options = models.JSONField(blank=True, default=list)  #use a json field since models doesnt support arrays
    multiple_choice_answers = models.JSONField(blank=True, default=list)
    single_choice_question = models.TextField(null=True, blank=True)
    single_choice_option = models.JSONField(blank=True, default=list)  #use a json field since models doesnt support arrays
    single_choice_answers = models.JSONField(blank=True, default=list)

    question_text = models.TextField(null=True, blank=True) # for generalised
    correct_answer = models.TextField(null=True, blank=True)  # maybe get rid of this too

    @property
    def poll_title(self):
        return self.poll.title
