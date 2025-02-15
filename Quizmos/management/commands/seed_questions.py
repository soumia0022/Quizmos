from django.core.management.base import BaseCommand
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
import random

from faker import Faker
from faker.providers import BaseProvider


class ComputingQuestionProvider(BaseProvider):
    def scq_question(self):
        questions = [
            ("What does CPU stand for?", ["Central Processing Unit", "Computer Personal Unit", "Central Process Utility", "Control Processing Unit"], "Central Processing Unit"),
            ("Which programming language is known for web development?", ["JavaScript", "C++", "Swift", "COBOL"], "JavaScript"),
            ("What is the main function of an operating system?", ["Manage hardware and software", "Browse the internet", "Run antivirus scans", "Edit documents"], "Manage hardware and software"),
            ("Who developed Python?", ["Guido van Rossum", "Microsoft", "Google", "IBM"], "Guido van Rossum"),
            ("What does RAM stand for?", ["Random Access Memory", "Read And Modify", "Rapid Application Manager", "Remote Access Module"], "Random Access Memory"),
            ("Which company developed the Windows operating system?", ["Microsoft", "Apple", "IBM", "Google"], "Microsoft"),
            ("Which of the following is a database management system?", ["MySQL", "Photoshop", "Windows", "Google Chrome"], "MySQL"),
            ("What does HTML stand for?", ["HyperText Markup Language", "High-Level Text Management Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], "HyperText Markup Language"),
            ("Which programming language is primarily used for Android app development?", ["Java", "Swift", "C#", "Python"], "Java"),
            ("What is an IP address used for?", ["Identifying devices on a network", "Storing files", "Processing graphics", "Running scripts"], "Identifying devices on a network"),
            ("What is the full form of GUI?", ["Graphical User Interface", "General User Input", "Graphical Uniform Interaction", "Global User Interface"], "Graphical User Interface"),
            ("Which programming paradigm is based on objects and classes?", ["Object-Oriented Programming", "Functional Programming", "Procedural Programming", "Logic Programming"], "Object-Oriented Programming"),
            ("What does DNS stand for?", ["Domain Name System", "Digital Network Service", "Data Navigation Structure", "Dynamic Naming System"], "Domain Name System"),
            ("What does LAN stand for?", ["Local Area Network", "Large Access Network", "Logical Application Node", "Long Area Net"], "Local Area Network"),
            ("Which of the following is an example of cloud storage?", ["Google Drive", "Microsoft Word", "Photoshop", "Notepad"], "Google Drive"),
            ("What does VPN stand for?", ["Virtual Private Network", "Visual Processing Node", "Verified Personal Network", "Variable Protocol Number"], "Virtual Private Network"),
            ("Which company developed the Linux kernel?", ["Linus Torvalds", "Microsoft", "Apple", "IBM"], "Linus Torvalds"),
            ("Which of the following is a NoSQL database?", ["MongoDB", "MySQL", "PostgreSQL", "Oracle DB"], "MongoDB"),
            ("Which of these is an example of cybersecurity software?", ["Antivirus", "Photoshop", "Excel", "VLC Media Player"], "Antivirus"),
            ("What is the purpose of an SSD?", ["Store data", "Process data", "Display graphics", "Run applications"], "Store data"),
            ("Which of the following is not a programming language?", ["Windows", "Python", "Java", "C++"], "Windows"),
            ("What does USB stand for?", ["Universal Serial Bus", "Uniform System Bridge", "Ultra Speed Buffer", "Universal Storage Block"], "Universal Serial Bus"),
            ("Which software is used for version control?", ["Git", "Excel", "Photoshop", "Microsoft Word"], "Git"),
            ("Which network topology has a central hub?", ["Star", "Bus", "Ring", "Mesh"], "Star"),
            ("Which key is used to refresh a webpage in most browsers?", ["F5", "Ctrl+R", "Alt+F4", "Shift+R"], "F5"),
            ("Which of the following is not a front-end framework?", ["Django", "React", "Angular", "Vue"], "Django"),
            ("What does GPU stand for?", ["Graphics Processing Unit", "General Processing Unit", "Global Program Utility", "Graphical Performance Unit"], "Graphics Processing Unit"),
            ("Which of these is a cybersecurity attack?", ["Phishing", "Compiling", "Rendering", "Encoding"], "Phishing"),
            ("Which protocol is used for secure web browsing?", ["HTTPS", "FTP", "SMTP", "TCP"], "HTTPS"),
            ("Which of the following is an example of an AI chatbot?", ["ChatGPT", "Microsoft Word", "Photoshop", "Excel"], "ChatGPT"),
            ("What is the purpose of a firewall?", ["Block unauthorized access", "Boost internet speed", "Store data", "Create backups"], "Block unauthorized access"),
            ("Which of these is not a cloud computing service?", ["RAM", "AWS", "Google Cloud", "Microsoft Azure"], "RAM"),
            ("What does IoT stand for?", ["Internet of Things", "Integrated Object Technology", "Internet of Transfers", "Interactive Online Tools"], "Internet of Things"),
            ("Which of these is not an operating system?", ["Oracle", "Linux", "Windows", "MacOS"], "Oracle"),
            ("Which of the following is a text editor?", ["VS Code", "Photoshop", "Excel", "PowerPoint"], "VS Code"),
            ("Which of these is a machine learning framework?", ["TensorFlow", "Django", "Spring Boot", "Bootstrap"], "TensorFlow"),
        ]

        question, options, answer = self.random_element(questions)
        random.shuffle(options)  # Shuffle the answer choices

        return {
            "question": question,
            "options": options,
            "correct_answer": answer
        }

    def mcq_question(self):
        questions = [
            ("What does CPU stand for?", ["Central Processing Unit", "Computer Personal Unit", "Central Process Utility", "Control Processing Unit"], ["Central Processing Unit"]),
            ("Which programming language is known for web development?", ["JavaScript", "C++", "Swift", "COBOL"], ["JavaScript"]),
            ("What is the main function of an operating system?", ["Manage hardware and software", "Browse the internet", "Run antivirus scans", "Edit documents"], ["Manage hardware and software"]),
            ("Which data structure uses FIFO (First In, First Out)?", ["Queue", "Stack", "Graph", "Tree"], ["Queue"]),
            ("Who developed Python?", ["Guido van Rossum", "Microsoft", "Google", "IBM"], ["Guido van Rossum"]),
            ("Which of these are interpreted languages?", ["Python", "C", "JavaScript", "C++"], ["Python", "JavaScript"]),
            ("What does RAM stand for?", ["Random Access Memory", "Read And Modify", "Rapid Application Manager", "Remote Access Module"], ["Random Access Memory"]),
            ("Which company developed the Windows operating system?", ["Microsoft", "Apple", "IBM", "Google"], ["Microsoft"]),
            ("Which of the following are database management systems?", ["MySQL", "Photoshop", "PostgreSQL", "Google Chrome"], ["MySQL", "PostgreSQL"]),
            ("What does HTML stand for?", ["HyperText Markup Language", "High-Level Text Management Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], ["HyperText Markup Language"]),
            ("Which programming languages are primarily used for Android app development?", ["Java", "Swift", "Kotlin", "Python"], ["Java", "Kotlin"]),
            ("What is an IP address used for?", ["Identifying devices on a network", "Storing files", "Processing graphics", "Running scripts"], ["Identifying devices on a network"]),
            ("Which company developed the Mac OS?", ["Apple", "Microsoft", "Linux Foundation", "IBM"], ["Apple"]),
            ("What is the purpose of a compiler?", ["Convert high-level code to machine code", "Execute programs", "Store data", "Debug applications"], ["Convert high-level code to machine code"]),
            ("Which data structures use LIFO (Last In, First Out)?", ["Stack", "Queue", "Graph", "Linked List"], ["Stack"]),
            ("What does HTTP stand for?", ["HyperText Transfer Protocol", "Hyperlink Text Processing", "High-Tech Transfer Protocol", "Hyperlink Transfer Process"], ["HyperText Transfer Protocol"]),
            ("Which of these are open-source operating systems?", ["Linux", "Windows", "MacOS", "Ubuntu"], ["Linux", "Ubuntu"]),
            ("Which programming paradigms are based on objects and classes?", ["Object-Oriented Programming", "Functional Programming", "Procedural Programming", "Logic Programming"], ["Object-Oriented Programming"]),
            ("Which of these are cybersecurity threats?", ["Phishing", "Compiling", "Malware", "SQL Injection"], ["Phishing", "Malware", "SQL Injection"]),
            ("Which of the following are markup languages?", ["HTML", "CSS", "Markdown", "Python"], ["HTML", "Markdown"]),
            ("Which network topologies are commonly used?", ["Star", "Bus", "Tree", "Pyramid"], ["Star", "Bus", "Tree"]),
            ("Which of the following are types of databases?", ["Relational", "NoSQL", "Hierarchical", "Blockchain"], ["Relational", "NoSQL", "Hierarchical"]),
            ("Which of these are cloud computing platforms?", ["AWS", "Google Cloud", "Photoshop", "Microsoft Azure"], ["AWS", "Google Cloud", "Microsoft Azure"]),
            ("Which programming languages are commonly used for AI development?", ["Python", "R", "Java", "HTML"], ["Python", "R", "Java"]),
            ("Which of these are valid IP address versions?", ["IPv4", "IPv6", "IPv8", "IPv2"], ["IPv4", "IPv6"]),
            ("What are common encryption algorithms?", ["AES", "RSA", "SHA-256", "PNG"], ["AES", "RSA", "SHA-256"]),
            ("Which of these are cybersecurity software?", ["Antivirus", "Firewall", "VPN", "Excel"], ["Antivirus", "Firewall", "VPN"]),
            ("Which of the following are front-end frameworks?", ["React", "Angular", "Django", "Vue"], ["React", "Angular", "Vue"]),
            ("Which of these are examples of version control systems?", ["Git", "SVN", "Mercurial", "FTP"], ["Git", "SVN", "Mercurial"]),
            ("What does CSS stand for?", ["Cascading Style Sheets", "Creative Styling System", "Computer Styling Script", "Coded Style Sheets"], ["Cascading Style Sheets"]),
            ("Which of these are Linux distributions?", ["Ubuntu", "Fedora", "Windows", "Debian"], ["Ubuntu", "Fedora", "Debian"]),
            ("Which of these are web browsers?", ["Chrome", "Firefox", "Edge", "Linux"], ["Chrome", "Firefox", "Edge"]),
            ("Which of the following are text editors?", ["VS Code", "Notepad++", "Photoshop", "Atom"], ["VS Code", "Notepad++", "Atom"]),
            ("Which of these are commonly used file compression formats?", ["ZIP", "RAR", "GZ", "TXT"], ["ZIP", "RAR", "GZ"])
        ]

        question, options, correct_answers = random.choice(questions)  # Randomly pick a question
        random.shuffle(options)  # Shuffle the answer choices

        return {
            "question": question,
            "options": options,
            "correct_answers": correct_answers
        }

# fake = Faker()
# fake.add_provider(ComputingQuestionProvider)


class Command(BaseCommand):
    """Build automation command to seed questions in the database"""

    QUESTION_PER_POLL = 7
    help = 'Seed the database with questions'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.faker.add_provider(ComputingQuestionProvider)

    def handle(self, *args, **options):
        self.create_questions()

    def create_questions(self):
        """Generate questions for each poll"""
        polls = Poll.objects.all()
        if not polls.exists():
            print("No polls found. Please seed polls first.")
            return

        for poll in polls:
            self.seed_questions_for_poll(poll)
            print(f"Seeded {self.QUESTION_PER_POLL} questions for poll '{poll.title}'                             ", end='\r')

    def seed_questions_for_poll(self, poll):
        """Generate 10 questions per poll, one for each type"""
        question_types = [
            'dropdown_fill',
            'text_fill',
            'multiple_choice',
            'single_choice',
            'wordcloud',
            'match_question',
            'code_question'
        ]

        for question_type in question_types:
            self.generate_question(poll, question_type)

        # Add three additional questions of random types to make it 10
        for _ in range(3):
            random_type = random.choice(question_types)
            self.generate_question(poll, random_type)

    def generate_question(self, poll, question_type):
        """Generate a question with realistic data based on type"""
        question_data = {
            'poll': poll,
            'question_type': question_type,
            'timer': random.choice([None, 30, 60, 120]),
        }

        if question_type == 'dropdown_fill':
            question_text = self.faker.sentence()
            words = question_text.split()  # Split sentence into words

            if len(words) > 1:  # Ensure there are enough words to replace one
                correct_word = random.choice(words)  # Pick a random word from the sentence
                question_text_with_blank = question_text.replace(correct_word, "____",
                                                                 1)  # Replace only first occurrence
            else:
                correct_word = words[0]  # Fallback in case of a single-word sentence
                question_text_with_blank = "____"

            # Generate distractor options including the correct answer
            options = list(set(self.faker.words(3) + [correct_word]))  # Ensure correct word is in options
            random.shuffle(options)  # Shuffle so correct answer isn't always first

            question_data.update({
                'question_text': question_text_with_blank,
                'dropdown_fill_question': question_text_with_blank,
                'dropdown_options': ', '.join(options),
                'dropdown_correct_answer': correct_word,
            })

        elif question_type == 'text_fill':
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'text_fill_question': question_text,
                'text_fill_answer': self.faker.word(),
            })

        elif question_type == 'multiple_choice':
            mcq = self.faker.mcq_question()

            question_data.update({
                'question_text': mcq['question'],
                'multiple_choice_question': mcq['question'],
                'multiple_choice_options': mcq['options'],
                'multiple_choice_answers': mcq['correct_answers'],
            })

        elif question_type == 'single_choice':
            scq = self.faker.scq_question()  # Get a computing question

            question_data.update({
                'question_text': scq['question'],
                'single_choice_question': scq['question'],
                'single_choice_option': scq['options'],
                'single_choice_answers': [scq['correct_answer']],  # The correct answer
            })

        elif question_type == 'wordcloud':
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'wordcloud_question': question_text,
            })

        elif question_type == 'match_question':
            options = self.faker.words(4)
            answers = self.faker.words(4)
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'match_question': question_text,
                'match_options': options,
                'match_answers': answers,
            })

        elif question_type == 'code_question':
            question_text = self.faker.sentence()
            question_data.update({
                'question_text': question_text,
                'code_question_text':question_text,
                'code_language': random.choice(["python", "javascript", "java"]),
                'code_test_cases': [{"input": "1 2", "output": "3"}, {"input": "3 3", "output": "6"}],
            })

        # Create question in the database
        Question.objects.create(**question_data)
