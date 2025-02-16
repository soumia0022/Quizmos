from django.http import JsonResponse
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

from response_management.models.response_model import MultipleChoiceResponse
from question_management.models.question_models import Question
import json

def get_question_response_counts(request, poll_code, question_id):


    question = Question.objects.filter(id=question_id).first()
    options = list(question.multiple_choice_options)


    responses = MultipleChoiceResponse.objects.filter(question=question).values_list('selected_options', flat=True)
    counts_dict = {i:0 for i in range(len(options))}

    for selected_values in responses:
        if isinstance(selected_values, str):

            selected_values = json.loads(selected_values)

        for selected_value in selected_values:
            if selected_value in options:
                selected_index = options.index(selected_value)
                counts_dict[selected_index] += 1



    return JsonResponse({
        'question_id': question_id,
        'counts': counts_dict
    })