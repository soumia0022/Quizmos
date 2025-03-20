from django.urls.conf import path
from response_management.views.get_student_answer import get_student_answer

urlpatterns = [
    path('get_answer/<int:poll_id>/<int:question_id>/', get_student_answer, name='get_student_answer'),
]