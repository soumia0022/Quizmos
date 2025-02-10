from django.urls.conf import path, include

from question_management.views.add_question import add_question
from question_management.views.edit_question import EditQuestionView
from question_management.views.delete_question import delete_question
from question_management.views.question_previews import question_preview, question_detail
from question_management.views.question_list import question_list

app_name = 'question_management'

question_patterns = [
    path('<int:question_id>/preview/', question_preview, name='question_preview'),
    path('<int:question_id>/', question_detail, name='question_detail'),
]

urlpatterns = [
    path('poll/<int:poll_id>/add-question/', add_question, name='add_question'),
    path('poll/<int:poll_id>/edit-question/', EditQuestionView.as_view(), name='edit_question'),
    path('poll/<int:poll_id>/delete-question/', delete_question, name='delete_question'),
    path('question/', include(question_patterns)),
    path('', question_list, name='question_list'),
]