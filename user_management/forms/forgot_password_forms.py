from allauth.account.forms import ResetPasswordForm
from ..utils import reverse_without_namespace  # custom resolver

class CustomResetPasswordForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        signup_url = reverse_without_namespace('account_signup')
        super().save(request, signup_url=signup_url, **kwargs)