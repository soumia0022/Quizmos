from django.urls.conf import path, include

from question_management.views import question_types
from question_management.views.question_types import add_question
from question_management.views.update_and_delete_question import edit_question, delete_question
from question_management.views import *

app_name = 'question_management'

question_patterns = [
    path('<int:question_id>/preview/', question_previews.question_preview, name='question_preview'),
    path('<int:question_id>/', question_previews.question_detail, name='question_detail'),
]

urlpatterns = [
    path('poll/<int:poll_id>/add-question/', add_question, name='add_question'),
    path('poll/<int:poll_id>/edit-question/', edit_question, name='edit_question'),
    path('poll/<int:poll_id>/delete-question/', delete_question, name='delete_question'),
    path('poll/<int:poll_id>/add-question/', question_types.add_question, name='add_question'),
    path('question/', include(question_patterns)),
    path('', question_list, name='question_list'),

]
