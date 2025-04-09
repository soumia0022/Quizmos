from django.urls.conf import path
from response_management.views.get_student_answer import get_student_answer
from response_management.views.student_view_response import student_view_poll
app_name = 'response_management'
urlpatterns = [
    path('get_answer/<int:poll_id>/<int:question_id>/', get_student_answer, name='get_student_answer'),
    path('student/view/<int:poll_id>/', student_view_poll, name='student_view_poll'),

]