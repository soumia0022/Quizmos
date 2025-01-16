from django.contrib import admin
from poll_management.models.poll_model import Poll

@admin.register(Poll)
class Poll(admin.ModelAdmin):
    list_display = ('title', )