# views.py
from allauth.account.views import PasswordResetView
from ..forms.forgot_password_forms import CustomResetPasswordForm  #custom form
from ..utils import reverse_without_namespace  # custom resolver

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomResetPasswordForm 

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        login_url = self.passthrough_next_url(reverse_without_namespace("account_login"))  
        signup_url = self.passthrough_next_url(reverse_without_namespace("account_signup"))  
        ret["password_reset_form"] = ret.get("form")
        ret.update({"login_url": login_url, "signup_url": signup_url})  
        return ret