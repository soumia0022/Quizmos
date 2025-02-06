from django.contrib import admin
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'submitted_on')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')
    ordering = ('-submitted_on',)

@admin.register(MultipleChoiceResponse)
class MultipleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'poll', 'submitted_on', 'selected_options')
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
    list_display = ('id','user', 'poll', 'submitted_on', 'selected_option')
    search_fields = ('question__text', 'user__username', 'poll__title')
    list_filter = ('submitted_on', 'poll')