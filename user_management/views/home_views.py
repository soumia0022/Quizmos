from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'about.html'

class FaqView(TemplateView):
    template_name = 'faq.html'