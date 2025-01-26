from django.urls.conf import path
from poll_management.views.create_poll import create_poll
from poll_management.views.poll_operation import poll_detail, poll_edit, poll_delete
from poll_management.views.join_poll import join_poll
from poll_management.views.display_code import display_code
from poll_management.views.poll_results import poll_results

app_name = 'poll_management'

urlpatterns = [
    path('create/', create_poll, name='create_poll'), 
    path('polls/create/', create_poll, name='create_poll'),
    path('<int:poll_id>/', poll_detail, name='poll_detail'),
    path('<int:poll_id>/edit/', poll_edit, name='poll_edit'),
    path('<int:poll_id>/delete/', poll_delete, name='poll_delete'),
    path('present/<int:pk>/', display_code, name= 'display_code'),
    path('join/<int:code>/', join_poll, name='join_poll'),
    path('results/<int:code>/', poll_results, name='poll_results')
]