from django import forms
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse

class MultipleChoiceResponseForm(forms.ModelForm):
    selected_options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)
    
    class Meta:
        model = MultipleChoiceResponse
        fields = ['selected_options']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if question:
            self.fields['selected_options'].choices = [(opt, opt) for opt in question.multiple_choice_options]

class SingleChoiceResponseForm(forms.ModelForm):
    selected_option = forms.ChoiceField(widget=forms.RadioSelect)
    
    class Meta:
        model = SingleChoiceResponse
        fields = ['selected_option']
        
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if question:
            self.fields['selected_option'].choices = [(opt, opt) for opt in question.single_choice_option]

class TextFillResponseForm(forms.ModelForm):
    class Meta:
        model = TextFillResponse
        fields = ['answer_text']

class DropdownFillResponseForm(forms.ModelForm):
    class Meta:
        model = DropdownFillResponse
        fields = ['selected_option']
        
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if question:
            self.fields['selected_option'].widget = forms.Select(choices=[(opt, opt) for opt in question.get_dropdown_options()])

class MatchQuestionResponseForm(forms.ModelForm):
    match_responses = forms.CharField(widget=forms.HiddenInput())   
    
    class Meta:
        model = MatchQuestionResponse
        fields = ['match_responses']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
