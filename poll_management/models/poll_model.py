from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    locked = models.BooleanField(default=False)
