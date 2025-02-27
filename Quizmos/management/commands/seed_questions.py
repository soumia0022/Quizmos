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

    def text_question(self):
        questions = [
            ("What does CPU stand for?", "Central Processing Unit"),
            ("Who developed Python?", "Guido van Rossum"),
            ("What is the primary function of an operating system?", "Manage hardware and software"),
            ("What does RAM stand for?", "Random Access Memory"),
            ("What is the full form of HTML?", "HyperText Markup Language"),
            ("Which programming language is mainly used for web development?", "JavaScript"),
            ("What does SQL stand for?", "Structured Query Language"),
            ("Which company developed the Windows operating system?", "Microsoft"),
            ("What is the purpose of a compiler?", "Convert high-level code to machine code"),
            ("What does HTTP stand for?", "HyperText Transfer Protocol"),
            ("Which data structure follows FIFO (First In, First Out)?", "Queue"),
            ("What is the function of an IP address?", "Identifying devices on a network"),
            ("Which company developed macOS?", "Apple"),
            ("What is the full form of GUI?", "Graphical User Interface"),
            ("Which protocol is used to send emails?", "SMTP"),
            ("What is the name of the person who created Linux?", "Linus Torvalds"),
            ("Which language is primarily used for Android app development?", "Java"),
            ("What does CSS stand for?", "Cascading Style Sheets"),
            ("What does DNS stand for?", "Domain Name System"),
            ("Which cloud storage service is offered by Google?", "Google Drive"),
            ("What does VPN stand for?", "Virtual Private Network"),
            ("What does USB stand for?", "Universal Serial Bus"),
            ("Which network topology uses a central hub?", "Star"),
            ("What key is commonly used to refresh a webpage?", "F5"),
            ("Which open-source operating system is widely used?", "Linux"),
            ("What is the purpose of an SSD?", "Store data"),
            ("Which software is used for version control?", "Git"),
            ("What does IoT stand for?", "Internet of Things"),
            ("Which programming language is mainly used for iOS app development?", "Swift"),
            ("Which protocol is used for secure web browsing?", "HTTPS"),
            ("What is the purpose of a firewall?", "Block unauthorized access"),
            ("What does ASCII stand for?", "American Standard Code for Information Interchange"),
            ("What programming paradigm is based on objects and classes?", "Object-Oriented Programming"),
            ("Which programming language is widely used in AI development?", "Python"),
            ("What is the full form of API?", "Application Programming Interface"),
            ("Which tool is used for writing and running Python code?", "Interpreter"),
            ("Which cybersecurity attack involves tricking people into revealing sensitive information?", "Phishing"),
            ("What is the term for software that manages databases?", "Database Management System"),
            ("What does LAN stand for?", "Local Area Network"),
            ("What is the default file extension for Python scripts?", ".py"),
            ("What is the name of the most widely used version control system?", "Git"),
            ("What is the primary function of a router?", "Direct network traffic"),
            ("What does ROM stand for?", "Read-Only Memory"),
            ("Which symbol is used to denote a comment in Python?", "#"),
            ("Which database type does MongoDB belong to?", "NoSQL"),
            ("Which programming language is used for machine learning and data science?", "Python"),
            ("Which cybersecurity method encrypts data for secure transmission?", "Cryptography"),
            ("What is the name of the main circuit board in a computer?", "Motherboard"),
            ("What does IP stand for?", "Internet Protocol"),
            ("Which unit is used to measure a computer's processing speed?", "Hertz"),
            ("What does URL stand for?", "Uniform Resource Locator"),
            ("What does FTP stand for?", "File Transfer Protocol"),
            ("Which search algorithm is used to find the shortest path in a graph?", "Dijkstra's Algorithm"),
            ("Which programming language was originally developed for system programming?", "C"),
            ("What does BIOS stand for?", "Basic Input Output System"),
            ("Which process converts source code into machine code?", "Compilation"),
            ("Which protocol is used for remote access to computers?", "SSH"),
            ("What does JSON stand for?", "JavaScript Object Notation"),
            ("Which machine learning library is developed by Google?", "TensorFlow"),
            ("What is the purpose of a cache in computing?", "Store frequently accessed data for faster retrieval"),
            ("Which Linux command is used to list files in a directory?", "ls"),
            ("What does RAID stand for?", "Redundant Array of Independent Disks"),
            ("What is the main purpose of a hash function in cryptography?", "Generate a unique fixed-length output for input data"),
            ("Which HTTP method is used to submit data to a server?", "POST"),
            ("What does CLI stand for?", "Command Line Interface"),
            ("What is the term for unwanted email messages?", "Spam"),
            ("Which programming language is most commonly used for game development?", "C++"),
            ("What does the term 'Big Data' refer to?", "Large and complex data sets that require advanced processing techniques"),
            ("Which component is responsible for executing instructions in a computer?", "Processor"),
            ("Which AI technique involves training computers to recognize patterns?", "Machine Learning"),
            ("What is the primary function of a web server?", "Serve web pages"),
            ("Which programming language is often used for statistical computing?", "R"),
            ("What is the default port number for HTTP?", "80"),
        ]

        question, answer = random.choice(questions)  # Select a random question
        return {
            "question": question,
            "correct_answer": answer
        }

    def wordcloud_question(self):
        questions = [
            "List popular programming languages.",
            "What are key components of a computer system?",
            "Name different types of data structures.",
            "What are common operating systems?",
            "List cybersecurity threats.",
            "Name major cloud computing platforms.",
            "What are common software development methodologies?",
            "List different types of network topologies.",
            "What are key principles of Object-Oriented Programming (OOP)?",
            "Name common database management systems.",
            "What are different types of computer memory?",
            "List famous computer scientists.",
            "Name common internet protocols.",
            "What are common Linux commands?",
            "List different programming paradigms.",
            "What are examples of artificial intelligence applications?",
            "Name popular front-end frameworks.",
            "List different cyber attack techniques.",
            "What are common HTTP status codes?",
            "Name essential software testing techniques.",
            "What are popular backend development frameworks?",
            "List key algorithms in computer science.",
            "What are components of an IP address?",
            "Name types of encryption algorithms.",
            "What are common network security tools?",
            "List different types of machine learning algorithms.",
            "What are key concepts in cloud computing?",
            "Name different types of programming errors.",
            "What are examples of embedded systems?",
            "List various types of computer peripherals."
        ]

        return {
            "question": self.random_element(questions)
        }

    def match_question(self):
        match_questions = [
            {
                "prompt": "Match the definitions",
                "options": ['Network', 'Node', 'Router', 'Packet'],
                "answers": ['A system of interconnected computers', 'A device that connects devices', 'A device used to forward data between devices', 'A unit of data transmitted over a network']
            },
            {
                "prompt": "Match the definitions",
                "options": ['RAM', 'CPU', 'Motherboard', 'Hard Drive'],
                "answers": ['Temporary data storage', 'Central processing unit', 'Main circuit board of a computer', 'Permanent data storage']
            },
            {
                "prompt": "Match the definitions",
                "options": ['DNS', 'IP Address', 'URL', 'HTTPS'],
                "answers": ['System to translate domain names into IP addresses', 'Unique identifier for a device on the network', 'Uniform Resource Locator, address of a web page', 'Secure version of HTTP']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Algorithm', 'Binary', 'Compiler', 'Encryption'],
                "answers": ['Step-by-step procedure to solve a problem', 'Number system with base 2', 'Converts source code into machine code', 'Process of securing data using a code']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Cloud Computing', 'Firewall', 'VPN', 'Malware'],
                "answers": ['Computing services provided over the internet', 'Network security system that monitors and controls incoming and outgoing traffic', 'Virtual private network that ensures private internet browsing', 'Software designed to harm or exploit computer systems']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Frontend', 'Backend', 'API', 'Database'],
                "answers": ['User-facing part of an application', 'Server-side processing and logic of an application', 'Interface for interaction between software applications', 'Collection of organized data for easy access, management, and updating']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Operating System', 'JavaScript', 'CSS', 'HTML'],
                "answers": ['Software that manages hardware and software resources', 'Scripting language for web development', 'Language for styling web pages', 'Markup language used to structure web pages']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Big Data', 'Machine Learning', 'Data Mining', 'AI'],
                "answers": ['Handling and analyzing large datasets', 'Subset of AI focused on learning from data', 'The process of discovering patterns in large datasets', 'Simulating human intelligence in machines']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Data Structure', 'Stack', 'Queue', 'Linked List'],
                "answers": ['A way to organize and store data for efficient access', 'A collection of elements with Last In First Out order', 'A collection of elements with First In First Out order', 'A linear data structure where elements are connected using pointers']
            },
            {
                "prompt": "Match the definitions",
                "options": ['IP Address', 'Packet Switching', 'Router', 'Bandwidth'],
                "answers": ['Unique identifier for a device on a network', 'Method of data transmission in which data is broken into small packets', 'A device that routes data between networks', 'The amount of data transferred over a network in a given time']
            },
            {
                "prompt": "Match the definitions",
                "options": ['HTTPS', 'URL', 'Web Browser', 'Web Server'],
                "answers": ['Secure version of HTTP for safe communication', 'Address used to access a resource on the web', 'Software application to browse the web', 'Software that hosts websites and services on the internet']
            },
            {
                "prompt": "Match the definitions",
                "options": ['JSON', 'SQL', 'XML', 'NoSQL'],
                "answers": ['A lightweight data interchange format', 'Structured Query Language for managing relational databases', 'Markup language for representing structured data', 'A non-relational database type for handling unstructured data']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Data Mining', 'IoT', 'Cloud Storage', 'Blockchain'],
                "answers": ['Process of analyzing large datasets to uncover hidden patterns', 'Interconnected network of devices exchanging data', 'Remote data storage accessible over the internet', 'A decentralized ledger for securely recording transactions']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Version Control', 'Compiler', 'Interpreter', 'Debugger'],
                "answers": ['Software that manages changes to source code over time', 'Software that translates source code into machine code', 'Software that executes code line by line', 'Software used to identify and fix errors in code']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Algorithm', 'Protocol', 'Cryptography', 'Firewall'],
                "answers": ['A set of rules for solving a problem or performing a task', 'A set of rules for communication between systems', 'The process of encoding information for secure transmission', 'A system for preventing unauthorized access to or from a network']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Cloud Computing', 'DNS', 'Firewall', 'Router'],
                "answers": ['Delivery of computing services over the internet', 'System that translates domain names into IP addresses', 'Security system that monitors and controls incoming and outgoing network traffic', 'Device used to forward data between devices on a network']
            },
            {
                "prompt": "Match the definitions",
                "options": ['HTML', 'CSS', 'JavaScript', 'PHP'],
                "answers": ['Markup language used to structure web pages', 'Style sheet language used to define the layout of web pages', 'Programming language for creating interactive web elements', 'Server-side scripting language used for web development']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Software', 'Hardware', 'Firmware', 'Middleware'],
                "answers": ['Programs and applications that run on a computer', 'Physical components of a computer system', 'Specialized software embedded in hardware', 'Software that connects different applications and systems']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Artificial Intelligence', 'Neural Networks', 'Deep Learning', 'Machine Learning'],
                "answers": ['Field of computer science focused on creating intelligent machines', 'Systems that simulate the human brain’s interconnected neurons', 'Subset of machine learning with multiple layers of abstraction', 'A type of machine learning where systems improve through data']
            },
            {
                "prompt": "Match the definitions",
                "options": ['JavaScript', 'Python', 'Ruby', 'C++'],
                "answers": ['A scripting language used for web development', 'A general-purpose programming language known for readability', 'A dynamic programming language used for web applications', 'A high-performance programming language commonly used for game development']
            },
            {
                "prompt": "Match the definitions",
                "options": ['Cache', 'Cookies', 'Server', 'Client'],
                "answers": ['Temporary storage used for quick data retrieval', 'Small pieces of data stored in a user’s browser', 'A system that provides resources or services to other computers', 'A device or software that requests resources from a server']
            }
        ]

        return self.random_element(match_questions)

    def dropdown_fill_in_the_blank(self):
        questions = [
            ("The brain of the computer is the ____.", ["CPU", "RAM", "Hard Drive", "Monitor"], "CPU"),
            ("____ is a programming language known for its simplicity and readability.", ["Python", "C++", "Java", "Assembly"], "Python"),
            ("The primary protocol used to transfer web pages is ____.", ["HTTP", "FTP", "SMTP", "SSH"], "HTTP"),
            ("A ____ is a collection of interrelated data.", ["Database", "Compiler", "Algorithm", "Cache"], "Database"),
            ("The OSI model has ____ layers.", ["7", "5", "3", "9"], "7"),
            ("The process of finding and fixing errors in code is called ____.", ["Debugging", "Compiling", "Testing", "Encrypting"], "Debugging"),
            ("In networking, ____ assigns IP addresses to devices dynamically.", ["DHCP", "DNS", "TCP", "SMTP"], "DHCP"),
            ("____ is the process of converting source code into machine code.", ["Compilation", "Interpretation", "Execution", "Encryption"], "Compilation"),
            ("A ____ is a type of malware that replicates itself and spreads.", ["Worm", "Firewall", "Trojan", "Antivirus"], "Worm"),
            ("The fastest type of memory in a computer is ____.", ["Cache", "RAM", "Hard Drive", "SSD"], "Cache"),
            ("A ____ is a set of rules for data communication.", ["Protocol", "Algorithm", "Function", "Database"], "Protocol"),
            ("The ____ controls how memory and processes are managed in a computer.", ["Operating System", "Router", "Compiler", "Cloud"], "Operating System"),
            ("The binary number system uses only ____ and ____.", ["0, 1", "1, 2", "0, 9", "A, B"], "0, 1"),
            ("An ____ converts human-readable code into machine code.", ["Compiler", "Debugger", "Firewall", "Cache"], "Compiler"),
            ("The programming language primarily used for web development is ____.", ["JavaScript", "C", "Python", "Swift"], "JavaScript"),
            ("A ____ is a placeholder for storing values in programming.", ["Variable", "Function", "Loop", "Class"], "Variable"),
            ("____ is used to uniquely identify devices on a network.", ["IP Address", "URL", "DNS", "MAC Address"], "IP Address"),
            ("The ____ tag is used to define a hyperlink in HTML.", ["<a>", "<p>", "<div>", "<h1>"], "<a>"),
            ("The ____ operator is used for logical AND in Python.", ["and", "&&", "||", "=="], "and"),
            ("A ____ is a sequence of characters in programming.", ["String", "Integer", "Boolean", "Float"], "String"),
            ("The term ____ refers to hiding implementation details in OOP.", ["Encapsulation", "Abstraction", "Inheritance", "Polymorphism"], "Encapsulation"),
            ("The main function in a C program is called ____.", ["main", "start", "execute", "run"], "main"),
            ("____ is a type of attack where data is intercepted during transmission.", ["Man-in-the-Middle", "Phishing", "DDoS", "Trojan"], "Man-in-the-Middle"),
            ("____ is used to prevent unauthorized access to or from a private network.", ["Firewall", "Malware", "Compiler", "Cache"], "Firewall")
        ]

        sentence, options, correct_answer = self.random_element(questions)  # Pick a random question
        random.shuffle(options)  # Shuffle options

        return {
            "sentence": sentence,
            "options": ", ".join(options),
            "correct_answer": correct_answer
        }

    def coding_question(self):
        questions = [
            "Write a Python function to check if a number is prime.",
            "Implement a program that reverses a string without using built-in functions.",
            "Create a function that finds the factorial of a number using recursion.",
            "Write a program to find the largest element in a list.",
            "Implement a sorting algorithm (e.g., Bubble Sort, Merge Sort, or Quick Sort).",
            "Create a simple calculator that performs basic arithmetic operations.",
            "Write a Python script to find the Fibonacci sequence up to N terms.",
            "Implement a function to check if a string is a palindrome.",
            "Write a function that counts the number of vowels in a given string.",
            "Create a program that simulates a basic banking system with deposit and withdrawal functions.",
            "Write a script to generate a random password with a mix of letters, numbers, and symbols.",
            "Implement a binary search algorithm.",
            "Write a program to find the GCD (Greatest Common Divisor) of two numbers.",
            "Create a function that removes duplicate elements from a list.",
            "Implement a program that checks if two strings are anagrams.",
            "Write a function to convert a decimal number to binary.",
            "Create a simple to-do list application using Python.",
            "Implement a function that finds the intersection of two lists.",
            "Write a Python script to scrape data from a website using BeautifulSoup.",
            "Create a program that simulates a dice roll.",
            "Write a function to find the second largest number in a list.",
            "Implement a basic chatbot using Python.",
            "Create a program that generates a multiplication table for a given number.",
            "Write a function that checks if a year is a leap year.",
            "Implement a simple login authentication system.",
            "Create a rock-paper-scissors game in Python.",
            "Write a function that returns the most common element in a list.",
            "Implement a basic text-based adventure game.",
            "Create a program that finds the longest common prefix in a list of strings.",
            "Write a function that generates a random sentence using a predefined word list.",
            "Implement a queue using stacks in Python.",
            "Create a function that finds the missing number in a list of consecutive numbers.",
            "Write a program that reads a file and counts the number of words.",
            "Implement a simple URL shortener.",
            "Create a Python program that fetches real-time weather data using an API.",
            "Write a function that finds all prime numbers up to a given number.",
            "Implement a basic file encryption and decryption script.",
            "Create a program that solves the Tower of Hanoi problem.",
            "Write a function that generates a random maze using recursion.",
            "Implement a simple markdown to HTML converter in Python.",
            "Create a Python program that sends an email using SMTP.",
            "Write a function that compresses a string using Run-Length Encoding (RLE).",
            "Implement a simple chatbot with predefined responses.",
            "Create a function that finds the longest palindrome in a given string.",
            "Write a Python program to simulate a traffic light system.",
            "Implement a function that finds the shortest path in a maze using BFS.",
            "Create a Python program that converts Roman numerals to integers.",
            "Write a function that validates an email address using regex.",
            "Implement a program that extracts metadata from an image file.",
            "Create a Python script that fetches the latest news headlines from an API.",
            "Write a program that generates a QR code for a given URL."
        ]

        question = self.random_element(questions)
        return question

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
            dropdown = self.faker.dropdown_fill_in_the_blank()  # Get a computing question

            question_data.update({
                'question_text': dropdown['sentence'],
                'dropdown_fill_question':  dropdown['sentence'],
                'dropdown_options': dropdown['options'],
                'dropdown_correct_answer': dropdown['correct_answer']
            })

        elif question_type == 'text_fill':
            text = self.faker.text_question()

            question_data.update({
                'question_text': text['question'],
                'text_fill_question': text['question'],
                'text_fill_answer': text['correct_answer'],
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
            question = self.faker.wordcloud_question()
            text = question['question']
            question_data.update({
                'question_text': text,
                'wordcloud_question': text,
            })

        elif question_type == 'match_question':
            question = self.faker.match_question()

            question_data.update({
                'question_text': question['prompt'],
                'match_question': question['prompt'],
                'match_options': question['options'],
                'match_answers': question['answers'],
            })

        elif question_type == 'code_question':
            question_text = self.faker.coding_question()
            question_data.update({
                'question_text': question_text,
                'code_question_text':question_text,
                'code_language': random.choice(["python", "javascript", "java"]),
                'code_test_cases': [{"input": "1 2", "output": "3"}, {"input": "3 3", "output": "6"}],
            })

        # Create question in the database
        Question.objects.create(**question_data)
