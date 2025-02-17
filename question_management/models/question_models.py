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
        ('code_question', 'Code Question'),
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
    dropdown_answer = models.TextField(null=True, blank=True)

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

    # Coding question fields
    code_question_text = models.TextField(null=True, blank=True)  # Prompt for the coding question
    code_language = models.CharField(max_length=20, default="python", null=True, blank=True)  # Programming language
    code_test_cases = models.JSONField(default=list, blank=True)  # JSON field for test cases


    audio_file = models.FileField(upload_to='uploads/audio/', null=True, blank=True)
    video_file = models.FileField(upload_to='uploads/video/', null=True, blank=True)
    youtube_link = models.URLField(max_length = 100, null=True, blank=True)

    @property
    def poll_title(self):
        return self.poll.title

    def get_dropdown_options(self):
        if not self.dropdown_options:
            options = []
        else:
            options = [opt.strip() for opt in self.dropdown_options.split(',') if opt.strip()]
            
        if self.dropdown_correct_answer and self.dropdown_correct_answer not in options:
            options.append(self.dropdown_correct_answer)        
        return options

# When refactoring models, use the below code:
# from django.db import models
# from poll_management.models.poll_model import Poll
#
#
# class Question(models.Model):
#     QUESTION_TYPES = [
#         ('dropdown_fill', 'Dropdown Fill in the Blank'),
#         ('text_fill', 'Text Answer'),
#         ('multiple_choice', 'Multiple Choice'),
#         ('single_choice', 'Single Choice'),
#         ('wordcloud', 'Word Cloud'),
#         ('match_question', 'Match Question'),
#         ('code_question', 'Code Question'),
#     ]
#
#     poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
#     question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
#     timer = models.IntegerField(null=True, blank=True, help_text="Time limit in seconds", default=None)
#     question_text = models.TextField(null=True, blank=True)  # General question text
#
#     class Meta:
#         abstract = True  # This model is abstract and will not be created as a table
#
#
# class MultipleChoiceQuestion(Question):
#     multiple_choice_question = models.TextField(null=True, blank=True)
#     multiple_choice_options = models.JSONField(blank=True, default=list)
#     multiple_choice_answers = models.JSONField(blank=True, default=list)
#
#
# class SingleChoiceQuestion(Question):
#     single_choice_question = models.TextField(null=True, blank=True)
#     single_choice_option = models.JSONField(blank=True, default=list)
#     single_choice_answers = models.JSONField(blank=True, default=list)
#
#
# class TextFillQuestion(Question):
#     text_fill_question = models.TextField(null=True, blank=True)
#     text_fill_answer = models.TextField(null=True, blank=True)
#
#
# class DropdownFillQuestion(Question):
#     dropdown_fill_question = models.TextField(null=True, blank=True)
#     dropdown_options = models.TextField(null=True, blank=True)  # Comma-separated options
#     dropdown_correct_answer = models.TextField(null=True, blank=True)
#     dropdown_answer = models.TextField(null=True, blank=True)
#
#
# class WordCloudQuestion(Question):
#     wordcloud_question = models.TextField(null=True, blank=True)
#
#
# class MatchQuestion(Question):
#     match_question = models.TextField(null=True, blank=True)
#     match_options = models.JSONField(blank=True, default=list)
#     match_answers = models.JSONField(blank=True, default=list)
#
#
# class CodeQuestion(Question):
#     code_question_text = models.TextField(null=True, blank=True)
#     code_language = models.CharField(max_length=20, default="python", null=True, blank=True)
#     code_test_cases = models.JSONField(default=list, blank=True)
