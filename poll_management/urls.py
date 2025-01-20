from django.urls.conf import path
from poll_management.views.create_poll import create_poll
from user_management.views.lecturer_dashboard import lecturer_dashboard

urlpatterns = [
    path('create/', create_poll, name='create_poll'),
    path('dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    path('polls/create/', create_poll, name='create_poll')
]