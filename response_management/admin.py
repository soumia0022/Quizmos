from django.contrib import admin
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse, WordCloudResponse, CodeQuestionResponse
from question_management.models.question_models import Question

def get_correct_answer(obj):
    """Retrieve the correct answer(s) for a given question."""
    if obj.question.question_type == "multiple_choice":
        return obj.question.multiple_choice_answers
    elif obj.question.question_type == "single_choice":
        return obj.question.single_choice_answers
    elif obj.question.question_type == "text_fill":
        return obj.question.text_fill_answer
    elif obj.question.question_type == "dropdown_fill":
        return obj.question.dropdown_correct_answer
    elif obj.question.question_type == "match_question":
        return obj.question.match_answers
    elif obj.question.question_type == "code_question":
        return obj.question.correct_code
    return "N/A"


@admin.register(MultipleChoiceResponse)
class MultipleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_options', 'question', 'session_code', 'is_correct', 'is_partially_correct',get_correct_answer)
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(SingleChoiceResponse)
class SingleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_option', 'question', 'session_code', 'is_correct', get_correct_answer)
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(TextFillResponse)
class TextFillResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'answer_text', 'session_code', 'is_correct', get_correct_answer)
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(DropdownFillResponse)
class DropdownFillResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_option', 'session_code', 'is_correct', get_correct_answer)
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(MatchQuestionResponse)
class MatchQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'match_responses', 'session_code', 'is_correct', 'is_partially_correct', get_correct_answer)
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(WordCloudResponse)
class WordCloudResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'word_cloud_response', 'session_code', 'is_correct', get_correct_answer)
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(CodeQuestionResponse)
class CodeQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'submitted_code', 'session_code', 'is_correct', get_correct_answer)
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')
