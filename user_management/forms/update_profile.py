"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from user_management.models.user_model import User
import os


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    @staticmethod
    def get_profile_pictures():
        pics_dir = os.path.join('static', 'profile_pics')
        categories = {
            'Galactic Heroes': [],
            'Celestial Wonders': [],
            'Mystical Orbs': [],
            'Intergalactic Visitors': []
        }
        for f in os.listdir(pics_dir):
            if f.endswith('.png'):
                if f.startswith('a'):
                    categories['Galactic Heroes'].append(f)
                elif f.startswith('s'):
                    categories['Celestial Wonders'].append(f)
                elif f.startswith('p'):
                    categories['Mystical Orbs'].append(f)
                elif f.startswith('u'):
                    categories['Intergalactic Visitors'].append(f)
        return categories

    categories = get_profile_pictures()
    profile_picture = forms.ChoiceField(choices=[(category, [(pic, pic) for pic in pictures])for category, pictures in categories.items()],required=False,label='Profile Picture')
    
    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture']


class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


