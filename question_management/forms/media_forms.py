from django import forms
from question_management.models.question_models import Question

class AudioUploadForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = Question
        fields = ['file', 'question']

class VideoUploadForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = Question
        fields = ['file', 'question']

class YouTubeLinkForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = Question
        fields = ['url', 'question']

