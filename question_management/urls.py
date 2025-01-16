from django.urls.conf import path
from question_management.views.question_types import create_poll, add_question, preview_question

urlpatterns = [
    path('create/', create_poll, name='create_poll'),
    path('poll/<int:poll_id>/add-question/', add_question, name='add_question'),
    path('preview/<int:poll_id>/preview/', preview_question, name='preview_question'),


]