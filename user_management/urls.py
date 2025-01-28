from django.conf import settings
from django.conf.urls.static import static
from django.urls import path ,include
from user_management.views import *
from django.contrib.auth import views as auth_views

reset_password_patterns = [
    path('reset/', auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

app_name = 'user_management'
urlpatterns = [
    path('', login_views.home, name='home'),
    path('dashboard/', login_views.dashboard, name='dashboard'),
    path('log_in/', login_views.LogInView.as_view(), name='log_in'),
    path('log_out/', login_views.log_out, name='log_out'),
    path('password/', profile_update_views.PasswordView.as_view(), name='password'),
    path('profile/', profile_update_views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', signup_views.SignUpView.as_view(), name='sign_up'),
    path('accounts/', include('allauth.urls')),
    path('accounts/password/', include(reset_password_patterns)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)