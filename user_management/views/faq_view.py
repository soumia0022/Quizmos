from django.views.generic import TemplateView

class FaqView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["faqs"] = {
            "general": [
                {"question": "How do Polls work?", "answer": "Polls are interactive questions that can be answered in real-time. Participants can submit their responses, and results are displayed instantly."},
                {"question": "Is the platform free?", "answer": "It is completely free to use."},
                {"question": "Do Polls work on all devices?", "answer": "Polls are designed to be responsive and work seamlessly across all devices, including smartphones, tablets, and desktops via the web browser."},
                {"question": "What should I do if I forget my account password?", "answer": "If you forget your password, you can use the 'Forgot Password' link on the login page to reset it. Follow the instructions sent to your email."},
                {"question": "How secure is my data?", "answer": "We take data security seriously. We never share your personal information with third parties."},
                {"question": "What types of questions are there?", "answer": "We support multiple question types including multiple choice, drag and drop, matching, and word clouds."},
            ],
            "students": [
                {"question": "How do I join a Poll?", "answer": "Enter the Poll code or scan the QR code shared with you."},
                {"question": "Do I need an account to participate?", "answer": "No, you can participate as a guest using just the Poll code or scanning the QR code. However, creating an account helps track your progress."},
                {"question": "Can I participate in a Poll at any time?", "answer": "No, you can only participate when the Poll has been started by the lecturer."},
                {"question": "How do I access Polls on my mobile device?", "answer": "You can access Polls via the web browser on your mobile device. Just enter the Poll code or scan the QR code."},
                {"question": "Can I see my past Poll results?", "answer": "Yes, if you have an account, all your Poll attempts and scores are saved in your dashboard."},
            ],
            "lecturers": [
                {"question": "How do I create a Poll?", "answer": "Log in to your account, and click the 'Create Poll' button. You can then select the type of questions you want and add them to your Poll."},
                {"question": "Can I reuse my Polls?", "answer": "Yes, all your Polls are saved in your dashboard and can be reused."},
                {"question": "How do I share my Poll with students?", "answer": "After creating your Poll, you will have the option to start the Poll. Once the Poll is started, you can display a Poll code and QR code that students can use to join."},
                {"question": "Can I export Poll results?", "answer": "Yes, you can export the results to a CSV file for further analysis or record-keeping."},
                {"question": "Can I embed media into the questions?", "answer": "Yes, you can add video, audio, and pictures into your questions."},
                {"question": "Can I set a time limit for my Poll?", "answer": "Yes, you can incorporate a timer into the questions."},
                {"question": "How do I view Poll analytics?", "answer": "Access detailed analytics for each Poll from your dashboard."},
            ],
        }

        return context