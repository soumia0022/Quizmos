from django.shortcuts import render, get_object_or_404
from poll_management.models.poll_model import Poll
from django.shortcuts import render, redirect
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.forms.submit_answer_form import MultipleChoiceResponseForm, SingleChoiceResponseForm, TextFillResponseForm, DropdownFillResponseForm


def poll_results(request, code):
    poll = get_object_or_404(Poll, number_code = code)

    form_classes = {
        'multiple_choice': MultipleChoiceResponseForm,
        'single_choice': SingleChoiceResponseForm,
        'text_fill': TextFillResponseForm,
        'dropdown_fill': DropdownFillResponseForm
    }

    if request.method == 'POST':
        form = MultipleChoiceResponseForm(request.POST)
        # form = FormClass(question, request.POST)
        if form.is_valid():
            print("form is valid")
            response = form.save(commit=False)
            #response.question = question
            # response.user = request.user
            response.poll = poll
            response.save()
        
        print("form is invalid")
    else:
        print("form is not post")
        # form = FormClass(question)

    return render(request, 'poll_results.html', {'poll': poll})