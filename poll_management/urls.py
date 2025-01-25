from django.urls.conf import path
from poll_management.views.create_poll import create_poll
from poll_management.views.poll_operation import poll_detail, poll_edit, poll_delete, poll_lock

urlpatterns = [
    path('create/', create_poll, name='create_poll'), 
    path('polls/create/', create_poll, name='create_poll'),
    path('<int:poll_id>/', poll_detail, name='poll_detail'),
    path('<int:poll_id>/edit/', poll_edit, name='poll_edit'),
    path('<int:poll_id>/delete/', poll_delete, name='poll_delete'),
    path('<int:poll_id>/lock/', poll_lock, name='poll_lock'),
]