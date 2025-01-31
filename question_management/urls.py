from django.urls.conf import path
from question_management.views.question_types import add_question
from question_management.views.update_and_delete_question import edit_question, delete_question

app_name = 'question_management'
urlpatterns = [
    path('poll/<int:poll_id>/add-question/', add_question, name='add_question'),
    path('poll/<int:poll_id>/edit-question/', edit_question, name='edit_question'),
    path('poll/<int:poll_id>/delete-question/', delete_question, name='delete_question'),
]
