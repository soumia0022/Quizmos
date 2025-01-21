from django.urls.conf import path
from poll_management.views.create_poll import create_poll
from poll_management.views.display_code import display_code

urlpatterns = [
    path('create/', create_poll, name='create_poll'),
    path('qr/<int:pk>/', display_code, name='display_code'),
]