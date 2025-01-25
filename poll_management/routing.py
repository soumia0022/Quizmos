from django.urls import re_path
from poll_management.consumers import PollConsumer

websocket_urlpatterns = [
    re_path(r'ws/poll/(?P<poll_code>\d+)/$', PollConsumer.as_asgi()),
]