from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from user_management.views import *
from user_management import views as home_views 

app_name = 'user_management'
urlpatterns = [
    path('', login_views.home, name='home'),
    path('dashboard/', login_views.dashboard, name='dashboard'),
    path('log_in/', login_views.LogInView.as_view(), name='log_in'),
    path('log_out/', login_views.log_out, name='log_out'),
    path('password/', profile_update_views.PasswordView.as_view(), name='password'),
    path('profile/', profile_update_views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', signup_views.SignUpView.as_view(), name='sign_up'),
    path('about/', home_views.AboutView.as_view(), name='about'),
    path('faq/', home_views.FaqView.as_view(), name='faq'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)