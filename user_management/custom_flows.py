from django.urls import reverse_lazy
from allauth.account.utils import build_absolute_uri

def get_signup_url(request):
    return build_absolute_uri(request, reverse_without_namespace("account_signup"))
