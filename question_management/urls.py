from django.urls.conf import path
from question_management.views.question_types import add_question

app_name = 'question_management'
urlpatterns = [
    path('poll/<int:poll_id>/add-question/', add_question, name='add_question'),

]
