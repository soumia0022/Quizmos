from django.conf import settings
from django.db import models
import random

class Poll(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('closed', 'Closed')], default='closed')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls')
    locked = models.BooleanField(default=False)
    number_code = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



    def __str__(self):
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