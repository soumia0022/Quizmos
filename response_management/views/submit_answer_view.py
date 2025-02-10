from django.shortcuts import render, redirect
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.forms.submit_answer_form import MultipleChoiceResponseForm, SingleChoiceResponseForm, TextFillResponseForm, DropdownFillResponseForm

def question_view(request, poll_id, question_id):
    question = Question.objects.get(id=question_id)
    poll = Poll.objects.get(id=poll_id)
    
    # form_classes = {
    #     'multiple_choice': MultipleChoiceResponseForm,
    #     'single_choice': SingleChoiceResponseForm,
    #     'text_fill': TextFillResponseForm,
    #     'dropdown_fill': DropdownFillResponseForm
    # }
    
    # FormClass = form_classes[question.question_type]

    if request.method == 'POST':
       
        form = MultipleChoiceResponseForm(request.POST)
        # form = FormClass(question, request.POST)
        if form.is_valid():
            print("form is valid")
            response = form.save(commit=False)
            response.question = question
            response.user = request.user
            response.poll = poll
            selected_options = form.cleaned_data['selected_options']
            response.selected_options = selected_options 
            response.save()
            
        print("form is invalid")
    else:
        print("form is not post")
        # form = FormClass(question)
    
    return render(request, 'question.html', {'form': form, 'question': question, 'poll': poll})