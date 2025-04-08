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
        form = self.form_class(initial={'uidb64': uidb64})
        get_token(request)  # Refresh CSRF token

        user = self._get_user_from_uidb64(uidb64)
        context = self._get_reset_context(user, token, form, uidb64)

        return render(request, self.template_name, context)

    def post(self, request, uidb64, token):
        user = self._get_user_from_uidb64(uidb64)
        form = self.form_class(request.POST, user=user)

        is_valid_token = user is not None and default_token_generator.check_token(user, token)

        if is_valid_token and form.is_valid() and form.save(uidb64, token, request):
            return redirect(self.success_url)

        context = self._get_reset_context(user, token, form, uidb64)
        return render(request, self.template_name, context)

    def _get_user_from_uidb64(self, uidb64):
        user_model = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            return None

    def _get_reset_context(self, user, token, form, uidb64):
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

        return {
            'form': form,
            'uidb64': uidb64,
            'token': token,
            'validlink': validlink,
            'title': title,
            'error_message': error_message,
            'token_fail': token_fail
        }