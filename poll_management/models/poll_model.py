from django.conf import settings
from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls')
    locked = models.BooleanField(default=False)
    number_code = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title
