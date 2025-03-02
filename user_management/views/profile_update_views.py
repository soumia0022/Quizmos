from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from user_management.forms.update_profile import  PasswordForm, UserForm
from django.contrib.auth import logout
from django.shortcuts import redirect



class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('user_management:dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    
    form_class = UserForm

    def dispatch(self, request, *args, **kwargs):
        """Block guest users from accessing profile update."""
        print(f"🔍 ProfileUpdateView triggered for: {request.path}")  # Debugging
        print(f"🔍 Request method: {request.method}")  # Debugging

        if request.user.first_name == "Guest":
            print("⚠️ Guest user detected! Logging them out.")  # Debugging
            logout(request)
            messages.info(request, "Guest users cannot edit profiles.")
            return redirect('user_management:home')  # Redirect guests to home

        return super

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


