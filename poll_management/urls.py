from django.urls.conf import path
from poll_management.views.create_poll import create_poll

urlpatterns = [
    path('create/', create_poll, name='create_poll'),
]