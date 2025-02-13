from django.urls.conf import path
from system_components.views.dashboard import return_to_dashboard

urlpatterns = [
    path('return-to-dashboard/', return_to_dashboard, name='return_to_dashboard'),

]