import requests
import json
import random
import pdfplumber
import docx
import re
import nltk
import time
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from question_management.views import QuestionManager
from poll_management.models.poll_model import Poll
from question_management.helpers import get_timer
from user_management.helpers import role_required

nltk.download('punkt')


OLLAMA_URL = 'http://localhost:11434/api/generate'
DEFAULT_MODEL = 'llama3.2'
MAX_PROMPT_LENGTH = 2000
TIMEOUT_SECONDS = 60


def extract_text_from_pdf(uploaded_file):
    """Extract text content from a PDF file"""
    print("Extracting text from PDF...")
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        print(f"Successfully extracted {len(text)} characters from PDF")
        return text.strip() if text.strip() else ""
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""


def extract_text_from_docx(uploaded_file):
    """Extract text content from a Word document"""
    print("Extracting text from DOCX...")
    text = ""
    try:
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
        print(f"Successfully extracted {len(text)} characters from DOCX")
        return text.strip() if text.strip() else ""
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
        return ""


def generate_with_ollama(prompt, model=DEFAULT_MODEL, temperature=0.7):
    """
    Generate text using the Ollama API.

    Args:
        prompt (str): The prompt to send to Ollama
        model (str): The model to use
        temperature (float): Temperature for generation

    Returns:
        str: The generated response
    """

    if len(prompt) > MAX_PROMPT_LENGTH:
        print(f"Prompt too long ({len(prompt)} chars), truncating to {MAX_PROMPT_LENGTH}")
        prompt = prompt[:MAX_PROMPT_LENGTH]

    print(f"Sending request to Ollama API (prompt length: {len(prompt)} chars)")
    start_time = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature
            },
            timeout=TIMEOUT_SECONDS
        )

        elapsed_time = time.time() - start_time
        print(f"Ollama API responded in {elapsed_time:.2f} seconds")

        if response.status_code == 200:
            response_json = json.loads(response.text)
            return response_json["response"]
        else:
            print(f"Error from Ollama API: Status code {response.status_code}")
            print(f"Response content: {response.text[:200]}...")
            return ""
    except requests.exceptions.Timeout:
        print(f"Timeout error: Ollama API call exceeded {TIMEOUT_SECONDS} seconds")
        return ""
    except Exception as e:
        print(f"Exception when calling Ollama API: {e}")
        return ""


def parse_multiple_choice_questions(text):
    """Extract complete multiple choice questions from text with improved robustness"""
    print("Parsing multiple choice questions...")
    questions = []


    full_q_pattern = r'(?:Question\s*(\d+):|Q(\d+):)\s*(.*?)(?=(?:Question\s*\d+:|Q\d+:|$))'
    question_matches = re.finditer(full_q_pattern, text, re.DOTALL)

    for q_match in question_matches:
        try:
            q_num = q_match.group(1) or q_match.group(2)
            q_content = q_match.group(3).strip()


            q_text_match = re.search(r'^(.*?)(?=\s*A[\.\)])', q_content, re.DOTALL)
            if not q_text_match:
                continue

            question_text = q_text_match.group(1).strip()
            if not question_text.endswith('?'):
                question_text += '?'


            options_text = q_content[q_text_match.end():].strip()


            options = []
            correct_answer = None


            option_pattern = r'([A-D])[\.\)]\s*(.*?)(?=\s*[A-D][\.\)]|\s*Correct Answer:|\s*$)'
            option_matches = re.finditer(option_pattern, options_text, re.DOTALL)

            for opt_match in option_matches:
                letter = opt_match.group(1)
                content = opt_match.group(2).strip()


                if content:
                    option = f"{letter}) {content}"
                    options.append(option)


            while len(options) < 4:
                letter = chr(65 + len(options))
                options.append(f"{letter}) Additional option")


            answer_match = re.search(r'Correct Answer:\s*([A-D])', q_content, re.DOTALL)
            if answer_match:
                letter = answer_match.group(1)
                for option in options:
                    if option.startswith(letter):
                        correct_answer = option
                        break


            if not correct_answer and options:
                correct_answer = options[0]


            questions.append({
                "question": question_text,
                "options": options[:4],
                "answer": correct_answer,
                "question_type": "multiple_choice"
            })
        except Exception as e:
            print(f"Error parsing question: {e}")
            continue


    if not questions:
        try:

            question_blocks = []
            current_block = ""

            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue


                if re.match(r'^(?:Question\s*\d+:|Q\d+:|\d+\.)', line):
                    if current_block:
                        question_blocks.append(current_block)
                    current_block = line
                else:
                    current_block += "\n" + line


            if current_block:
                question_blocks.append(current_block)


            for block in question_blocks:
                try:

                    q_match = re.search(r'^(?:Question\s*\d+:|Q\d+:|\d+\.)\s*(.*?)(?=\s*A[\.\)])', block, re.DOTALL)
                    if not q_match:
                        continue

                    question_text = q_match.group(1).strip()
                    if not question_text.endswith('?'):
                        question_text += '?'


                    options_text = block[q_match.end():].strip()
                    options = []


                    option_matches = re.finditer(r'([A-D])[\.\)]\s*(.*?)(?=\s*[A-D][\.\)]|\s*Correct|$)', options_text,
                                                 re.DOTALL)
                    for match in option_matches:
                        letter = match.group(1)
                        content = match.group(2).strip()
                        if content:
                            options.append(f"{letter}) {content}")


                    while len(options) < 4:
                        letter = chr(65 + len(options))
                        options.append(f"{letter}) Additional option")


                    correct_answer = None
                    answer_match = re.search(r'Correct Answer:\s*([A-D])', block, re.DOTALL)
                    if answer_match:
                        letter = answer_match.group(1)
                        for option in options:
                            if option.startswith(letter):
                                correct_answer = option
                                break


                    if not correct_answer and options:
                        correct_answer = options[0]

                    questions.append({
                        "question": question_text,
                        "options": options[:4],
                        "answer": correct_answer,
                        "question_type": "multiple_choice"
                    })
                except Exception as e:
                    print(f"Error in alternative parsing: {e}")
                    continue
        except Exception as e:
            print(f"Error in fallback parsing: {e}")

    print(f"Successfully parsed {len(questions)} questions")
    return questions


def generate_simple_questions(text, num_questions=5):
    """
    Generate simple multiple choice questions using Ollama.
    Simplified version with better error handling and improved prompts.
    """
    print(f"Generating {num_questions} questions from text ({len(text)} chars)")


    if len(text) < 1000:
        prompt = f"""
Generate {num_questions} multiple-choice quiz questions based on this text:
{text}

CRITICAL INSTRUCTIONS:
1. Each option MUST be COMPLETE in itself - DO NOT split information across options!
2. Make sure options are properly formatted with A), B), C), D) at the beginning
3. NEVER continue one option into another option
4. DO NOT split long distances or measurements

Example of CORRECT formatting:
Question 1: How far can a tiger's roar be heard?
A) Up to 3 kilometers (2 miles)
B) Up to 5 kilometers (3 miles)
C) Up to 8 kilometers (5 miles)
D) More than 10 kilometers (6 miles)
Correct Answer: B

Example of INCORRECT formatting (DO NOT DO THIS):
Question 1: How far can a tiger's roar be heard?
A) Up to 3 kilometers
B) (2 miles)
C) Up to 5 kilometers
D) (3 miles)

Format each question EXACTLY as shown in the correct example.
"""

        generated_text = generate_with_ollama(prompt, temperature=0.7)
        if generated_text:
            questions = parse_multiple_choice_questions(generated_text)
            if questions:
                return questions


    if len(text) > 1000:
        print("Text is long, using first 1000 characters")
        prompt = f"""
Generate {num_questions} multiple-choice quiz questions based on this text:
{text[:1000]}

CRITICAL INSTRUCTIONS:
1. Each option MUST be COMPLETE in itself - DO NOT split information across options!
2. Make sure options are properly formatted with A), B), C), D) at the beginning
3. NEVER continue one option into another option
4. DO NOT split long distances or measurements

Example of CORRECT formatting:
Question 1: How far can a tiger's roar be heard?
A) Up to 3 kilometers (2 miles)
B) Up to 5 kilometers (3 miles)
C) Up to 8 kilometers (5 miles)
D) More than 10 kilometers (6 miles)
Correct Answer: B

Example of INCORRECT formatting (DO NOT DO THIS):
Question 1: How far can a tiger's roar be heard?
A) Up to 3 kilometers
B) (2 miles)
C) Up to 5 kilometers
D) (3 miles)

Format each question EXACTLY as shown in the correct example.
"""


        generated_text = generate_with_ollama(prompt, temperature=0.7)
        if generated_text:
            questions = parse_multiple_choice_questions(generated_text)
            if questions:
                return questions


    print("Using fallback questions")
    return fallback_questions(num_questions)


def fallback_questions(num_questions=5):
    """Provide fallback questions when generation fails"""
    questions = [
        {
            "question": "What is the main topic of this document?",
            "options": [
                "A) Historical events and figures",
                "B) Scientific concepts and discoveries",
                "C) Literary analysis and criticism",
                "D) Technical instructions and guidelines"
            ],
            "answer": "A) Historical events and figures",
            "question_type": "multiple_choice"
        },
        {
            "question": "Which category would this document most likely belong to?",
            "options": [
                "A) Academic textbook",
                "B) News article",
                "C) Informational guide",
                "D) Research paper"
            ],
            "answer": "C) Informational guide",
            "question_type": "multiple_choice"
        },
        {
            "question": "What is the primary purpose of this document?",
            "options": [
                "A) To inform about a specific topic",
                "B) To persuade the reader to take action",
                "C) To entertain through storytelling",
                "D) To analyze complex data"
            ],
            "answer": "A) To inform about a specific topic",
            "question_type": "multiple_choice"
        },
        {
            "question": "What reading level would this document be appropriate for?",
            "options": [
                "A) Elementary school",
                "B) Middle school",
                "C) High school",
                "D) College level"
            ],
            "answer": "C) High school",
            "question_type": "multiple_choice"
        },
        {
            "question": "How would you best describe the writing style of this document?",
            "options": [
                "A) Formal and academic",
                "B) Casual and conversational",
                "C) Technical and specialized",
                "D) Narrative and descriptive"
            ],
            "answer": "A) Formal and academic",
            "question_type": "multiple_choice"
        }
    ]

    return questions[:num_questions]


@login_required
@role_required('Lecturer')
def add_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)

    if request.method == 'POST' and 'file' in request.FILES:
        print("File upload detected")
        uploaded_file = request.FILES['file']
        text_content = ""


        print("Testing Ollama API connection...")
        test_response = generate_with_ollama("Generate one simple question about tigers.", temperature=0.5)
        print(f"Ollama test response received: {len(test_response)} chars")


        if uploaded_file.name.endswith('.pdf'):
            text_content = extract_text_from_pdf(uploaded_file)
            print(f"Extracted PDF content length: {len(text_content)} characters")
        elif uploaded_file.name.endswith(('.docx', '.doc')):
            text_content = extract_text_from_docx(uploaded_file)
            print(f"Extracted document content length: {len(text_content)} characters")
        else:
            print(f"Unsupported file format: {uploaded_file.name}")
            return JsonResponse({"error": "Unsupported file format."})

        if text_content.strip():
            print("Generating questions from extracted text...")

            generated_questions = generate_simple_questions(text_content)

            if generated_questions:
                print(f"Successfully generated {len(generated_questions)} questions")
                return JsonResponse({"questions": generated_questions})
            else:
                print("Failed to generate questions")
                return JsonResponse({"error": "Failed to generate questions. Please try again."})
        else:
            print("No text content extracted from file")
            return JsonResponse({"error": "No text could be extracted from the file."})

    if request.method == 'POST' and 'file' not in request.FILES:
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