from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.middleware.csrf import get_token
from user_management.forms.forgot_password_forms import CustomSetPasswordForm

class CustomPasswordResetConfirmView(View):
    form_class = CustomSetPasswordForm
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('user_management:dashboard')

    def get(self, request, uidb64, token):
        form = self.form_class()
        get_token(request)  # Refresh CSRF token
        return render(request, self.template_name, {'form': form, 'uidb64': uidb64, 'token': token})

    def post(self, request, uidb64, token):
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.save(uidb64, token, request):
                return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'uidb64': uidb64, 'token': token})