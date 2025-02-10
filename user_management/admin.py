from django.contrib import admin
from user_management.models import User

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)