from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["mission"] = "Our mission is to facilitate the exchange of ideas and thoughts through engaging polls. We aim to make learning content accessible and fun, helping lecturers spark curiosity and encourage participation in the classroom. We believe in making learning an interactive, collaborative, and enjoyable experience. Quizmos empowers educators and learners to create, share, and participate in engaging poll-based learning activities."
        
        context["journey"] =  " ".join ([
            "Founded in 2025, Quizmos started as a simple tool to make learning more engaging.",
            "Our adventure began with a different name and theme, Pollinators. Inspired by the industrious and collaborative nature of bees, we created a platform for buzzing discussions and poll-driven insights.",
            "However, as our community grew and evolved, so did our vision. We realized that the scope of our mission extended beyond any single theme.",
            "Thus, we launched into a new era with a space theme, becoming Quizmos. Just as space exploration inspires curiosity and wonder, we strive to uncover new insights and trends that shape our world."
        ])

        context["features"] = [
            {"icon": "fas fa-clock", "text": "Real-time polling and quiz creation"},
            {"icon": "fas fa-brain", "text": "Interactive learning experiences"},
            {"icon": "fas fa-puzzle-piece", "text": "Easy-to-use platform for educators and learners"},
            {"icon": "fas fa-chart-pie", "text": "Instant result tracking and analytics"},
        ]

        context["values"] = [
            {"icon": "fas fa-lightbulb", "text": "Innovation: Continuously improving and adapting"},
            {"icon": "fas fa-handshake", "text": "Integrity: Honest and transparent in all actions"},
            {"icon": "fas fa-users", "text": "Collaboration: Working together for better results"},
            {"icon": "fas fa-trophy", "text": "Excellence: Striving for the highest quality"},
        ]

        context["team"] = [
            {"name": "Amina Ali", "role": "Technical Analyst", "quote": "Innovation drives progress."},
            {"name": "Rashida Begum", "role": "UX Designer", "quote": "Technology is the key to unlocking our potential."},
            {"name": "Soumia Bekhli", "role": "CEO & Founder", "quote": "Empowering education through technology is our mission."},
            {"name": "Alishba Faisal", "role": "Lead Developer", "quote": "Every challenge is an opportunity to innovate."},
            {"name": "Leyli Jalilova", "role": "Operations Manager", "quote": "Our journey is defined by the impact we create."},
            {"name": "Eeshal Malik", "role": "Project Manager", "quote": "Collaboration and creativity drive our success."},
            {"name": "Marium Rukiya", "role": "Quality Assurance Engineer", "quote": "Transforming education, one poll at a time."},
        ]

        context["reviews"] = [
            {"stars": 5, "text": "Quizmos has revolutionized how I engage with my students. The real-time feedback is invaluable!", "author": "Sarah Johnson, King's College London Lecturer"},
            {"stars": 5, "text": "Easy to use and incredibly effective for keeping students engaged during classes.", "author": "Michael Chen, University Professor"},
            {"stars": 5, "text": "Lectures are much more enjoyable when Quizmos is involved!", "author": "Hanna Smith, Student"},
            {"stars": 4.5, "text": "The analytics help us track engagement effectively.", "author": "Emily Roberts, Teaching Assistant"},
        ]

        return context