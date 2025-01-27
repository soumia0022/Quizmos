from django.conf import settings
from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('closed', 'Closed')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls')

    def _str_(self):
        return self.title

class Response(models.Model):
    poll = models.ForeignKey(
        Poll, related_name='response', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)