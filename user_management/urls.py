from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from user_management.views.about_view import AboutView
from user_management.views.faq_view import FaqView
from user_management.forms.forgot_password_forms import CustomPasswordResetForm
from user_management.views.profile_update_views import delete_account
from user_management.views import (
    guest_logout,
    login_views,
    profile_update_views,
    signup_views,
    forgot_password_views,
    archive_view
)

app_name = 'user_management'

reset_password_patterns = [
    path('reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html',
    form_class=CustomPasswordResetForm , success_url=reverse_lazy('user_management:password_reset_done')), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', forgot_password_views.CustomPasswordResetConfirmView.as_view(template_name='account/password_reset_from_key.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns = [
    path('', login_views.home, name='home'),
    path('dashboard/', login_views.dashboard, name='dashboard'),
    path('log_in/', login_views.LogInView.as_view(), name='log_in'),
    path('log_out/', login_views.log_out, name='log_out'),
    path('password/', profile_update_views.PasswordView.as_view(), name='password'),
    path('profile/', profile_update_views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', signup_views.SignUpView.as_view(), name='sign_up'),
    path('accounts/password/', include(reset_password_patterns)),
    path('guest_logout/', guest_logout.logout_and_login, name='guest_logout'),
    path('about/', AboutView.as_view(), name='about'),
    path("faq/", FaqView.as_view(), name="faq"),
    path('delete-account/', delete_account, name='delete_account'),
    path('poll/<int:poll_id>/archive/', archive_view.archive_poll, name='archive_poll'),
    path('poll/<int:poll_id>/unarchive/', archive_view.unarchive_poll, name='unarchive_poll'),
    path('poll/<int:poll_id>/toggle_archive/', archive_view.toggle_archive_poll, name='toggle_archive_poll'),
    path('polls/archived/', archive_view.view_archived_polls, name='view_archived_polls'),



]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
