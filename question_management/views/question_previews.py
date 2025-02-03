from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from question_management.models.question_models import Question
from django.shortcuts import render

def question_preview(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    preview_data = {
        'question_type': question.get_question_type_display(),
        'timer': question.timer,
        'question_text': question.question_text,
    }
    return JsonResponse(preview_data)

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'question_detail.html', context)


