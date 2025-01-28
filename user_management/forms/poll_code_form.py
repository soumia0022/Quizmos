from django import forms
from poll_management.models.poll_model import Poll

class PollCodeForm(forms.Form):
    poll_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Poll Code',
            'required': True
        })
    )


    def validate_and_redirect(self):
        poll_code = self.cleaned_data['poll_code']
        poll = Poll.objects.filter(number_code=poll_code).first()
        if poll:
            return True, poll
        else:
            self.add_error('poll_code', 'Invalid poll code')
            return False, None
