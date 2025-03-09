from django.contrib import admin
from django import forms
from question_management.models.question_models import Question



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['poll', 'question_type', 'text_fill_question', 'dropdown_fill_question', 'dropdown_options',
                  'multiple_choice_question', 'multiple_choice_options', 'single_choice_question',
                  'single_choice_option', 'dropdown_correct_answer','wordcloud_question','code_question_text', 'code_language', 'correct_code']

    # Override the form to conditionally show/hide fields based on the question type
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        question_type = self.instance.question_type if self.instance else None

        # Hide all fields initially
        self.fields['text_fill_question'].widget.attrs['style'] = 'display:none;'
        self.fields['text_fill_answer'].widget.attrs['style'] = 'display:none;'

        self.fields['dropdown_fill_question'].widget.attrs['style'] = 'display:none;'
        self.fields['dropdown_options'].widget.attrs['style'] = 'display:none;'

        self.fields['multiple_choice_question'].widget.attrs['style'] = 'display:none;'
        self.fields['multiple_choice_options'].widget.attrs['style'] = 'display:none;'

        self.fields['single_choice_question'].widget.attrs['style'] = 'display:none;'
        self.fields['single_choice_option'].widget.attrs['style'] = 'display:none;'
        self.fields['word_cloud_question'].widget.attrs['style'] = 'display:none;'


        self.fields['code_question_text'].widget.attrs['style'] = 'display:none;'
        self.fields['code_language'].widget.attrs['style'] = 'display:none;'
        self.fields['correct_code'].widget.attrs['style'] = 'display:none;'


        if question_type == 'text_fill':
            self.fields['text_fill_question'].widget.attrs['style'] = ''
            self.fields['text_fill_answer'].widget.attrs['style'] = ''

        elif question_type == 'dropdown_fill':
            self.fields['dropdown_fill_question'].widget.attrs['style'] = ''
            self.fields['dropdown_options'].widget.attrs['style'] = ''
            self.fields['dropdown_correct_answer'].widget.attrs['style'] = ''

        elif question_type == 'multiple_choice':
            self.fields['multiple_choice_question'].widget.attrs['style'] = ''
            self.fields['multiple_choice_options'].widget.attrs['style'] = ''
            self.fields['multiple_choice_answers'].widget.attrs['style'] = ''

        elif question_type == 'single_choice':
            self.fields['single_choice_question'].widget.attrs['style'] = ''
            self.fields['single_choice_option'].widget.attrs['style'] = ''
            self.fields['single_choice_answers'].widget.attrs['style'] = ''

        elif question_type == 'match_question':
            self.fields['match_question'].widget.attrs['style'] = ''
            self.fields['match_options'].widget.attrs['style'] = ''
            self.fields['match_answers'].widget.attrs['style'] = ''

        elif question_type == 'word_cloud':
            self.fields['wordcloud_question'].widget.attrs['style'] = ''

        elif question_type == 'code_question':
            self.fields['code_question_text'].widget.attrs['style'] = ''
            self.fields['code_language'].widget.attrs['style'] = ''
            self.fields['correct_code'].widget.attrs['style'] = ''


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = (
        'poll', 'poll_title', 'question_type', 'question_timer',
        'text_fill_question', 'text_fill_answer','dropdown_fill_question', 'dropdown_options','dropdown_correct_answer',
        'multiple_choice_question', 'multiple_choice_options', 'multiple_choice_answers',
        'single_choice_question', 'single_choice_option', 'single_choice_answers',
        'match_question', 'match_options', 'match_answers', 'code_question_text', 'code_language', 'correct_code',
        'wordcloud_question', 'audio_file', 'video_file', 'image_file', 'youtube_link'
    )
    list_filter = ('poll', 'question_type')
    search_fields = ('text_fill_question', 'dropdown_fill_question', 'multiple_choice_question',
                     'single_choice_question', 'match_question','wordcloud_question')

# Display fields based on the question type
    def get_fields(self, request, obj=None):
        fields = ['poll', 'question_type']

        if obj and obj.question_type == 'text_fill':
            fields.extend(['text_fill_question','question_timer'])
        elif obj and obj.question_type == 'dropdown_fill':
            fields.extend(['dropdown_fill_question', 'dropdown_options','question_timer'])
        elif obj and obj.question_type == 'multiple_choice':
            fields.extend(['multiple_choice_question', 'multiple_choice_options','question_timer'])
        elif obj and obj.question_type == 'single_choice':
            fields.extend(['single_choice_question', 'single_choice_option', 'question_timer'])
        elif obj and obj.question_type == 'word_cloud':
            fields.extend(['wordcloud_question', 'question_timer'])


        return fields


admin.site.register(Question, QuestionAdmin)


