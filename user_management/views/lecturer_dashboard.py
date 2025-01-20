from django.shortcuts import render, redirect
from poll_management.models.poll_model import Poll
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

@login_required
def lecturer_dashboard(request):
    return render(request, 'lecturer_dashboard.html')