from django.contrib import admin
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse, WordCloudResponse, CodeQuestionResponse

@admin.register(MultipleChoiceResponse)
class MultipleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_options', 'question', 'session_code')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(SingleChoiceResponse)
class SingleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_option', 'session_code')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(TextFillResponse)
class TextFillResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'answer_text', 'session_code')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(DropdownFillResponse)
class DropdownFillResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_option', 'session_code')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(MatchQuestionResponse)
class MatchQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'match_responses', 'session_code')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(WordCloudResponse)
class WordCloudResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'word_cloud_response', 'session_code')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(CodeQuestionResponse)
class CodeQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'submitted_code', 'session_code')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')