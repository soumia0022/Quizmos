from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MatchQuestionResponse
import json

def poll_results(request, code):
    poll = get_object_or_404(Poll, number_code=code)
    question = Question.objects.filter(poll=poll).first() 


    if request.method == 'POST':

        if question.question_type == 'match_question':
            match_responses = request.POST.get('match_responses', '{}') 
                        
            try:
                match_responses_json = json.loads(match_responses)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
            match_response = MatchQuestionResponse.objects.create(
                user=request.user,
                poll=poll,
                question=question, 
                match_responses=match_responses_json
            )
            match_response.save()
            
            print(f"Stored match_responses: {match_responses_json}")
            return redirect('poll_management:poll_results', code=poll.number_code)
    
    return render(request, 'poll_results.html', {'poll': poll})
