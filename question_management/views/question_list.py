from django.shortcuts import render

from question_management.models.question_models import Question

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})