from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MatchQuestionResponse, MultipleChoiceResponse, SingleChoiceResponse, DropdownFillResponse, TextFillResponse
import json

def poll_results(request, code):
    poll = get_object_or_404(Poll, number_code=code)
    
    if request.method == 'POST':
        question_processed = set()
        for question in poll.questions.all():
            if question.question_type in question_processed:
                continue

            if question.question_type == 'match_question':
                match_responses = request.POST.get('match_responses', '{}')
                try:
                    match_responses_json = json.loads(match_responses)
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON data for match responses'}, status=400)
                
                if match_responses_json:
                    MatchQuestionResponse.objects.create(
                        user=request.user,
                        poll=poll,
                        question=question,
                        match_responses=match_responses_json
                    )
                question_processed.add(question.question_type)

            elif question.question_type == 'multiple_choice':
                multiple_choice_responses = request.POST.get('multiple_choice_responses', '[]')
                if multiple_choice_responses and multiple_choice_responses != '[]':
                    try:
                        multiple_choice_responses_json = json.loads(multiple_choice_responses)
                    except json.JSONDecodeError:
                        return JsonResponse({'error': 'Invalid JSON data for multiple-choice responses'}, status=400)
                        
                    if multiple_choice_responses_json:
                        MultipleChoiceResponse.objects.create(
                            user=request.user,
                            poll=poll,
                            question=question,
                            selected_options=multiple_choice_responses_json
                        )
                question_processed.add(question.question_type)

            elif question.question_type == 'single_choice':
                single_choice_response = request.POST.get('single_choice_response', '')
                if single_choice_response:
                    SingleChoiceResponse.objects.create(
                        user=request.user,
                        poll=poll,
                        question=question,
                        selected_option=single_choice_response
                    )
                question_processed.add(question.question_type)

            elif question.question_type == 'dropdown_fill':
                dropdown_response = request.POST.get('dropdown_response', '')
                if dropdown_response:
                    DropdownFillResponse.objects.create(
                        user=request.user,
                        poll=poll,
                        question=question,
                        selected_option=dropdown_response
                    )
                question_processed.add(question.question_type)

            elif question.question_type == 'text_fill':
                text_fill_response = request.POST.get('text_fill_response', '')
                if text_fill_response:
                    TextFillResponse.objects.create(
                        user=request.user,
                        poll=poll,
                        question=question,
                        answer_text=text_fill_response
                    )
                question_processed.add(question.question_type)

        return redirect('poll_management:poll_results', code=poll.number_code)

    question = Question.objects.filter(poll=poll).first()  
    return render(request, 'poll_results.html', {'poll': poll, 'question': question})
