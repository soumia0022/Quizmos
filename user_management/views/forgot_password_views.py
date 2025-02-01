# user_management/views/forgot_password_views.py
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.middleware.csrf import get_token
from user_management.forms.forgot_password_forms import CustomSetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

class CustomPasswordResetConfirmView(View):
    form_class = CustomSetPasswordForm
    template_name = 'account/password_reset_complete.html'
    success_url = reverse_lazy('user_management:dashboard')

    def get(self, request, uidb64, token):
        form = self.form_class()
        get_token(request)  # Refresh CSRF token
        user_model = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            validlink = True
            title = 'Enter new password'
            error_message = ''
            token_fail = False
        else:
            validlink = False
            title = 'Password reset unsuccessful'
            error_message = 'The password reset link was invalid.'
            token_fail = True

        return render(request, self.template_name, {
            'form': form,
            'uidb64': uidb64,
            'token': token,
            'validlink': validlink,
            'title': title,
            'error_message': error_message,
            'token_fail': token_fail
        })

    def post(self, request, uidb64, token):
        form = self.form_class(request.POST)
        user_model = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            validlink = True
            if form.is_valid():
                if form.save(uidb64, token, request):
                    return redirect(self.success_url)
            title = 'Enter new password'
            error_message = ''
            token_fail = False
        else:
            validlink = False
            title = 'Password reset unsuccessful'
            error_message = 'The password reset link was invalid.'
            token_fail = True

        return render(request, self.template_name, {
            'form': form,
            'uidb64': uidb64,
            'token': token,
            'validlink': validlink,
            'title': title,
            'error_message': error_message,
            'token_fail': token_fail
        })
