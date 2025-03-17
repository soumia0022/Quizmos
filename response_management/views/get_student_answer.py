from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from question_management.models.question_models import Question
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, DropdownFillResponse, TextFillResponse, WordCloudResponse, CodeQuestionResponse  
)

@login_required
@csrf_exempt
def get_student_answer(request, poll_id, question_id):
    """Fetch student's selected answer and correct answer"""
    if request.method == "GET":
        user = request.user  # Logged-in student

        # Fetch the correct answer from the Question model
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({"error": "Question not found"}, status=404)

        correct_answer = None
        if question.question_type == 'multiple_choice':
            correct_answer = question.multiple_choice_answers
            if isinstance(correct_answer, str): 
                correct_answer = [correct_answer]
        elif question.question_type == 'single_choice':
            correct_answer = question.single_choice_answers
        elif question.question_type == 'dropdown_fill':
            correct_answer = question.dropdown_correct_answer
        elif question.question_type == 'text_fill':
            correct_answer = question.text_fill_answer
        elif question.question_type == 'match_question':
            try:
                match_options = question.match_options or []
                match_answers = question.match_answers or []
                if len(match_options) != len(match_answers):
                    correct_answer = "Mismatch between options and answers"
                else:
                    correct_answer = [
                        {"left": option, "right": answer}
                        for option, answer in zip(match_options, match_answers)
                    ]
            except Exception as e:
                return JsonResponse({"error": f"Error processing match answers: {str(e)}"}, status=500)
        elif question.question_type == 'code_question':
            correct_answer = question.correct_code
        else:
            correct_answer = "No correct answer available"

        # Fetch student's selected answer from Response models
        response = None
        response_models = {
            'multiple_choice': MultipleChoiceResponse,
            'single_choice': SingleChoiceResponse,
            'dropdown_fill': DropdownFillResponse,
            'text_fill': TextFillResponse,
            'code_question': CodeQuestionResponse,  
        }

        if question.question_type in response_models:
            response_model = response_models[question.question_type]
            response = response_model.objects.filter(user=user, question=question, poll_id=poll_id).first()

        student_answer = None
        if response:
            if hasattr(response, "selected_option"):
                student_answer = response.selected_option
            elif hasattr(response, "selected_options"):
                student_answer = response.selected_options
            elif hasattr(response, "answer_text"):
                student_answer = response.answer_text
            
            elif hasattr(response, "submitted_code"):  
                student_answer = response.submitted_code
        elif question.question_type == 'word_cloud':
                response = WordCloudResponse.objects.filter(user=user, question=question, poll_id=poll_id).first()
                student_answer = response.word_cloud_response if response and response.word_cloud_response else None




        return JsonResponse({
            "question_id": question_id,
            "question_type": question.question_type,  
            "selected_answer": student_answer,
            "correct_answer": correct_answer
        })

    return JsonResponse({"error": "Invalid request method"}, status=400)