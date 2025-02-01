from django import forms
from user_management.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.core.exceptions import ValidationError
import re

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            self.fields['email'].error_messages['invalid'] = 'No user is registered with this email address. Please sign up.'
        return email

    def save(self, request, **kwargs):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        use_https = kwargs.get('use_https', False)
        email_template_name = kwargs.get('email_template_name')
        token_generator = kwargs.get('token_generator', default_token_generator)
        from_email = kwargs.get('from_email')
        subject_template_name = kwargs.get('subject_template_name')
        extra_email_context = kwargs.get('extra_email_context')

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            subject = 'Password Reset'
            message = f'Click the link to reset your password: {request.build_absolute_uri(reverse("user_management:password_reset_confirm", kwargs={"uidb64": uid, "token": token}))}'
            send_mail(subject, message, from_email, [email])
        else:
            subject = 'Sign Up'
            message = f'You are not registered. Click the link to sign up: {request.build_absolute_uri(reverse_lazy("user_management:sign_up"))}'
            send_mail(subject, message, from_email, [email])

    def reset_password(self, uidb64, token, new_password, request):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            login(request, user)
            return True
        return False


class CustomSetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        password_confirm = cleaned_data.get("new_password_confirm")

        if not password or not password_confirm:
            raise ValidationError("Both password fields are required.")

        if password != password_confirm:
            raise ValidationError("Passwords do not match.")

        # Basic password validation: at least 8 characters, one number, one uppercase, one lowercase
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
            raise ValidationError("Password must be at least 8 characters long, contain one number, one uppercase, and one lowercase letter.")

        # Ensure the new password is not the same as the old password
        if self.user and self.user.check_password(password):
            raise ValidationError("New password cannot be the same as the old password.")

        return cleaned_data

    def save(self, uidb64, token, request):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.set_password(self.cleaned_data['new_password'])
            user.save()
            login(request, user)
            return True
        return False

