from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import random
import pdfplumber
import docx
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from question_management.views import QuestionManager
from poll_management.models.poll_model import Poll
from question_management.helpers import get_timer
from user_management.helpers import role_required
import nltk

nltk.download('punkt')


model_name = "google/flan-t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)



def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip() if text.strip() else ""



def extract_text_from_docx(uploaded_file):
    text = ""
    doc = docx.Document(uploaded_file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip() if text.strip() else ""


def generate_questions_from_text(text):
    """
    Generate multiple-choice questions from text.

    Args:
        text (str): The input text to generate questions from

    Returns:
        list: List of dictionaries containing questions, options and answers
    """
    import random

    cleaned_text = " ".join(text.split())
    sentences = nltk.sent_tokenize(cleaned_text)
    questions = []


    valid_sentences = [s for s in sentences if len(s.split()) >= 6]


    for sentence in valid_sentences[:5]:
        if not sentence.strip():
            continue

        words = sentence.split()
        for i, word in enumerate(words):

            if len(word) >= 4 and i > 0 and i < len(words) - 1:

                question_text = " ".join(words[:i] + ["_____"] + words[i + 1:]) + "?"


                if word[0].isupper():
                    distractors = ["Paris", "London", "Berlin", "Madrid", "Rome", "Dublin",
                                   "England", "France", "Germany", "Spain", "Italy", "Scotland"]

                    distractors = [d for d in distractors if d != word]

                    distractors = random.sample(distractors, min(3, len(distractors)))
                else:

                    similar_words = [w for w in set(words) if len(w) >= 4 and w != word]
                    if len(similar_words) >= 3:
                        distractors = random.sample(similar_words, 3)
                    else:
                        distractors = ["option", "choice", "alternative"]


                options = [f"A. {word}"]


                for j, distractor in enumerate(distractors[:3]):
                    options.append(f"{chr(66 + j)}. {distractor}")


                while len(options) < 4:
                    options.append(f"{chr(65 + len(options))}. Additional option")

                questions.append({
                    "question": question_text,
                    "options": options,
                    "answer": options[0]
                })


                break

    return questions


def parse_generated_question(text, original_sentence):
    """
    This function is kept for compatibility but no longer used.
    Our question generation now handles everything directly.
    """
    try:
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        question = lines[0].strip()
        if not question.endswith('?'):
            question += '?'

        options = []
        correct_answer = None

        for line in lines[1:]:
            if line.startswith(('A.', 'B.', 'C.', 'D.', 'A)', 'B)', 'C)', 'D)')):
                option = line.strip()
                options.append(option)

                if 'CORRECT' in line.upper():
                    correct_answer = option

        if not correct_answer and options:
            last_line = lines[-1].upper()
            if "CORRECT" in last_line or "ANSWER" in last_line:
                for opt in "ABCD":
                    if opt in last_line:
                        for option in options:
                            if option.startswith(f"{opt}.") or option.startswith(f"{opt})"):
                                correct_answer = option
                                break

        if not correct_answer and options:
            correct_answer = options[0]

        while len(options) < 4:
            options.append(f"Option {chr(65 + len(options))}. Additional choice")

        return {
            "question": question,
            "options": options,
            "answer": correct_answer
        }
    except Exception as e:
        print(f"Error parsing generated question: {e}")
        return None


@login_required
@role_required('Lecturer')
def add_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    generated_questions = []

    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        text_content = ""

        if uploaded_file.name.endswith('.pdf'):
            text_content = extract_text_from_pdf(uploaded_file)
            print(f"Extracted PDF content (first 500 chars): {text_content[:500]}")
        elif uploaded_file.name.endswith(('.docx', '.doc')):
            text_content = extract_text_from_docx(uploaded_file)
            print(f"Extracted DOCX content (first 500 chars): {text_content[:500]}")
        else:
            return JsonResponse({"error": "Unsupported file format."})

        if text_content.strip():
            generated_questions = generate_questions_from_text(text_content)

        if generated_questions:
            return JsonResponse({"questions": generated_questions})
        else:
            return JsonResponse({"error": "No questions could be generated from the document."})

    if request.method == 'POST' and not 'file' in request.FILES:
        manager = QuestionManager(request, poll_id, request.POST.get('youtube_link'), get_timer(request))

        if manager.question_type == 'text_fill':
            response = manager.handle_text_fill()
        elif manager.question_type == 'dropdown_fill':
            response = manager.handle_dropdown_fill()
        elif manager.question_type == 'multiple_choice':
            response = manager.handle_multiple_choice()
        elif manager.question_type == 'single_choice':
            response = manager.handle_single_choice()
        elif manager.question_type == 'wordcloud':
            wordcloud_image = manager.handle_wordcloud()
            return render(request, "add_question.html", {"poll": poll, "wordcloud_image": wordcloud_image})
        elif manager.question_type == 'match_question':
            response = manager.handle_match_question()
        elif manager.question_type == "code_question":
            response = manager.handle_code_question()

        if isinstance(response, JsonResponse):
            return response

        return redirect("question_management:add_question", poll_id=poll.id)

    return render(request, "add_question.html", {"poll": poll})