from django.views.generic import TemplateView

class FaqView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["faqs"] = {
            "general": [
                {"question": "How do Quizzes work?", "answer": "Quizzes have interactive questions that can be answered in real-time. Participants can submit their responses, and results are displayed instantly."},
                {"question": "Is the platform free?", "answer": "It is completely free to use."},
                {"question": "Can I use the platform without an internet connection?", "answer": "No, an active internet connection is required to access and participate in Quizzes."},
                {"question": "Do Quizzes work on all devices?", "answer": "Quizzes are designed to be responsive and work seamlessly across all devices, including smartphones, tablets, and desktops via the web browser."},
                {"question": "How secure is my data?", "answer": "We take data security seriously. We never share your personal information with third parties."},
                {"question": "What types of questions are there?", "answer": "We support a variety of question types including single choice, multiple choice, dropdown, matching, coding and word cloud."},
            ],
            
            "students": [
                {"question": "How do I join a Quiz?", "answer": "Enter the numerical 6 digit code or scan the QR code shared with you."},
                {"question": "Do I need an account to participate?", "answer": "No, you can participate as a guest using just the numerical code or scanning the QR code. However, creating an account helps track your progress."},
                {"question": "Can I participate in a Quiz at any time?", "answer": "No, you can only participate when the Quiz has been started by the lecturer."},
                {"question": "How do I access Quizzes on my mobile device?", "answer": "You can access Quizzes via the web browser on your mobile device. Just enter the numerical code or scan the QR code."},
                {"question": "Can I change my answers after submitting them?", "answer": "You can continue to submit answers to change your response to a question until the time limit is reached, or the lecturer locks the question."},
                {"question": "Can I see my past Quiz results?", "answer": "Yes, if you have an account, all your Quiz attempts are saved in your dashboard."},
                {"question": "Can I view all my attempts to the same Quiz?", "answer": "Yes, simply select the 'view responses' button, and if you answered the same Quiz more than once you will be prompted to select the session code to view a specific attempt."},
            ],

            "lecturers": [
                {"question": "How do I create a Quiz?", "answer": "Log in to your account, and click the 'Create Quiz' button. You can then select the type of questions you want and add them to your Quiz."},
                {"question": "How many questions can be added to a Quiz?", "answer": "A maximum of 20 questions per Quiz."},
                {"question": "Can I reuse my Quiz?", "answer": "Yes, all your Quizzes are saved in your dashboard and can be reused."},
                {"question": "Can I preview my Quiz before sharing it?", "answer": "Yes, in the edit page of a particular Quiz, you can preview how each question will be displayed to the student"},
                {"question": "How do I share my Quiz with students?", "answer": "After creating your Quiz, you will have the option to start the Quiz. Once the Quiz is started, you can display a numerical code and QR code that students can use to join."},
                {"question": "Can I export Quiz results?", "answer": "Yes, you can export the results to a CSV file for further analysis or record-keeping."},
                {"question": "Can I embed media into the questions?", "answer": "Yes, you can add video, audio, and pictures into your questions."},
                {"question": "How do I view Quiz analytics?", "answer": "Access detailed analytics for each Quiz from your dashboard."},
                {"question": "How to temporarily stop response submission when hosting a Quiz?", "answer": "You can lock the Quiz to prevent further submissions from students. You can then unlock the Quiz to allow responses once again"},
                {"question": "Can I set a time limit for my Quiz?", "answer": "Yes, you can incorporate a timer into the questions. Once the timer runs out during a question, the Quiz will automatically lock."},
                {"question": "How can I show the correct answer to the students during the Quiz?", "answer": "When hosting a Quiz, there is an eye icon above each question. When clicked, it displays the correct answer options to the students."},
            ],
        }

        return context
