from django.urls.conf import path, include
from question_management.views import *

app_name = 'question_management'

question_patterns = [
    path('<int:question_id>/preview/', question_previews.question_preview, name='question_preview'),
    path('<int:question_id>/', question_previews.question_detail, name='question_detail'),
]

urlpatterns = [
    path('poll/<int:poll_id>/add-question/', question_types.add_question, name='add_question'),
    path('question/', include(question_patterns)),
    path('', question_list, name='question_list'),
]
