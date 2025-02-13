from django.contrib import admin
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse

@admin.register(MultipleChoiceResponse)
class MultipleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_options', 'question')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(SingleChoiceResponse)
class SingleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_option')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(TextFillResponse)
class TextFillResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'answer_text')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(DropdownFillResponse)
class DropdownFillResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'selected_option')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')

@admin.register(MatchQuestionResponse)
class MatchQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on', 'match_responses')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')
