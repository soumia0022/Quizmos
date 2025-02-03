from django.urls.conf import path
from poll_management.views.create_poll import create_poll
from poll_management.views.join_poll import join_poll
from poll_management.views.display_code import display_code
from poll_management.views.poll_results import poll_results
from poll_management.views.poll_operation import view_poll  


app_name = 'poll_management'
from poll_management.views.poll_operation import poll_edit, poll_delete, poll_lock

urlpatterns = [
    path('create/', create_poll, name='create_poll'), 
    path('polls/create/', create_poll, name='create_poll'),
    path('<int:poll_id>/edit/', poll_edit, name='poll_edit'),
    path('<int:poll_id>/delete/', poll_delete, name='poll_delete'),
    path('present/<int:pk>/', display_code, name= 'display_code'),
    path('join/<int:code>/', join_poll, name='join_poll'),
    path('results/<int:code>/', poll_results, name='poll_results'),
    path('<int:poll_id>/lock/', poll_lock, name='poll_lock'),
    path('poll/view/<int:poll_id>/', view_poll, name='view_poll'),
]