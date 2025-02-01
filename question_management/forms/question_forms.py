from django import forms
from question_management.models.question_models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_text', 'question_type', 'text_fill_question', 'text_fill_answer',
            'dropdown_fill_question', 'dropdown_options', 'multiple_choice_question',
            'multiple_choice_options', 'multiple_choice_answers', 'single_choice_question',
            'single_choice_option', 'single_choice_answers', 'wordcloud_question', 'match_question',
            'match_options', 'match_answers', 'timer', 'audio_file', 'video_file', 'youtube_link'
        ]
