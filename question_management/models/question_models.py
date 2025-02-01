from django.db import models
from poll_management.models.poll_model import Poll

class Question(models.Model):
    QUESTION_TYPES = [
        ('dropdown_fill', 'Dropdown Fill in the Blank'), # database name, display name
        ('text_fill', 'Text Answer'),
        ('multiple_choice', 'Multiple Choice'),
        ('single_choice', 'Single Choice'),
        ('wordcloud', 'Word Cloud'),
        ('match_question', 'Match Question'),
    ]
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE, default=1) # question associated w poll
                                        # related name questions to allow you to do something like poll.questions.all() to get
                                        # all qs for that poll
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')

    # Timer field (time in seconds)
    timer = models.IntegerField(null=True, blank=True, help_text="Time limit in seconds", default=None)


    # Fields for different question types
    text_fill_question = models.TextField(null=True, blank=True)
    text_fill_answer = models.TextField(null=True, blank=True)

    dropdown_fill_question = models.TextField(null=True, blank=True)
    dropdown_options = models.TextField(null=True, blank=True)  # comma-separated options for dropdown
    dropdown_correct_answer = models.TextField(null=True, blank=True)

    multiple_choice_question = models.TextField(null=True, blank=True)
    multiple_choice_options = models.JSONField(blank=True, default=list)  #use a json field since models doesnt support arrays
    multiple_choice_answers = models.JSONField(blank=True, default=list)

    single_choice_question = models.TextField(null=True, blank=True)
    single_choice_option = models.JSONField(blank=True, default=list)  #use a json field since models doesnt support arrays
    single_choice_answers = models.JSONField(blank=True, default=list)

    wordcloud_question = models.TextField(null=True, blank=True)

    match_question = models.TextField(null=True, blank=True)
    #the index of the option will match up with the index of the answer
    match_options = models.JSONField(blank=True, default=list)
    match_answers = models.JSONField(blank=True, default=list)

    question_text = models.TextField(null=True, blank=True) # for generalised

    @property
    def poll_title(self):
        return self.poll.title

    def get_dropdown_options(self):
        return self.dropdown_options.split(',') if self.dropdown_options else []