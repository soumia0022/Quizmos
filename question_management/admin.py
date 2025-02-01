from django.contrib import admin
from django import forms
from question_management.models.question_models import Question



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['poll', 'question_type', 'text_fill_question', 'dropdown_fill_question', 'dropdown_options',
                  'multiple_choice_question', 'multiple_choice_options', 'single_choice_question',
                  'single_choice_option', 'dropdown_correct_answer']

    # Override the form to conditionally show/hide fields based on the question type
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        question_type = self.instance.question_type if self.instance else None

        # Hide all fields initially
        self.fields['text_fill_question'].widget.attrs['style'] = 'display:none;'
        self.fields['dropdown_fill_question'].widget.attrs['style'] = 'display:none;'
        self.fields['dropdown_options'].widget.attrs['style'] = 'display:none;'
        self.fields['multiple_choice_question'].widget.attrs['style'] = 'display:none;'
        self.fields['multiple_choice_options'].widget.attrs['style'] = 'display:none;'
        self.fields['single_choice_question'].widget.attrs['style'] = 'display:none;'
        self.fields['single_choice_option'].widget.attrs['style'] = 'display:none;'

        if question_type == 'text_fill':
            self.fields['text_fill_question'].widget.attrs['style'] = ''
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

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = ('poll', 'poll_title', 'question_type', 'timer',
                    'text_fill_question', 'dropdown_fill_question', 'dropdown_options', 'dropdown_correct_answer',
                    'multiple_choice_question', 'multiple_choice_options', 'multiple_choice_answers',
                    'single_choice_question', 'single_choice_option', 'single_choice_answers',
                    'match_question', 'match_options', 'match_answers')
    list_filter = ('poll', 'question_type')
    search_fields = ('text_fill_question', 'dropdown_fill_question', 'multiple_choice_question',
                     'single_choice_question', 'match_question')


# Display fields based on the question type
    def get_fields(self, request, obj=None):
        fields = ['poll', 'question_type']

        if obj and obj.question_type == 'text_fill':
            fields.extend(['text_fill_question','timer'])
        elif obj and obj.question_type == 'dropdown_fill':
            fields.extend(['dropdown_fill_question', 'dropdown_options','timer'])
        elif obj and obj.question_type == 'multiple_choice':
            fields.extend(['multiple_choice_question', 'multiple_choice_options','timer'])
        elif obj and obj.question_type == 'single_choice':
            fields.extend(['single_choice_question', 'single_choice_option', 'timer'])

        return fields


admin.site.register(Question, QuestionAdmin)


