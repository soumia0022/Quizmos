"""
URL configuration for Quizmos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls.conf import include

import user_management

urlpatterns = [
    path('admin/', admin.site.urls),
    path('questions/', include('question_management.urls')),
    path('polls/', include('poll_management.urls')),
    path('responses/', include('response_management.urls')),
    path('analytics/', include('analytics.urls')),
    path('', include('user_management.urls')),
    path('accounts/', include('allauth.urls')),
]
