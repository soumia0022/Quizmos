from django.urls.conf import path
from poll_management.views.create_poll import create_poll
from user_management.views.lecturer_dashboard import lecturer_dashboard
from poll_management.views.poll_list import poll_list
from poll_management.views.poll_operation import poll_detail, poll_edit, poll_delete




urlpatterns = [
    path('list/', poll_list, name='poll_list'),
    path('create/', create_poll, name='create_poll'),
    path('dashboard/', lecturer_dashboard, name='lecturer_dashboard'),  
    path('polls/create/', create_poll, name='create_poll'),
    path('<int:poll_id>/', poll_detail, name='poll_detail'),
    path('<int:poll_id>/edit/', poll_edit, name='poll_edit'),
    path('<int:poll_id>/delete/', poll_delete, name='poll_delete')   
]