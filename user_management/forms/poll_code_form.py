from django import forms
from poll_management.models.poll_model import Poll

class PollCodeForm(forms.Form):
    poll_code = forms.IntegerField(
        min_value=100000,
        max_value=999999,
        error_messages={
            'min_value': 'Ensure this value has at least 6 characters',
            'max_value': 'Ensure this value has no more than 6 characters.'
        },
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
