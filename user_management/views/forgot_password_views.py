from user_management.models.user_model import User
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.shortcuts import render
from user_management.forms.forgot_password import CustomPasswordResetForm

def password_reset(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    url = request.build_absolute_uri(reverse('account_reset_password_from_key', kwargs={'uidb64': uid, 'token': token}))
                    context = {
                        "user": user,
                        "url": url,
                    }
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    email_content = render_to_string(email_template_name, context)
                    send_mail(subject, email_content, None, [user.email])
            return HttpResponse(_("Password reset e-mail has been sent."))
    else:
        form = CustomPasswordResetForm()
    
    return render(request, "password_reset_form.html", {"form": form})
