from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[
        MinLengthValidator(3, "Username must be at least 3 characters long."),
        RegexValidator(r'^[a-zA-Z0-9]+$', "Username must only contain letters and numbers."),
        RegexValidator(r'^(?=.*[a-zA-Z])', "Username must contain at least one letter.")
        ]
    )
    
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)

    ROLES = [('Student', 'Student'), ('Lecturer', 'Lecturer'),]
    role = models.CharField(max_length=10, choices=ROLES, default='Student', blank=False)
    profile_picture = models.CharField(max_length=100, blank=True, null=True, default='default.jpeg')

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""

        return self.gravatar(size=60)