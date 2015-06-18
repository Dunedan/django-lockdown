from django import forms


class CustomLockdownForm(forms.Form):

    """A form to test the behavior of using custom forms for authentication."""

    answer = forms.IntegerField()

    def clean_answer(self):
        """Cleaning of the answer field, by checking it's value."""
        if self.cleaned_data['answer'] == 42:
            return 42
        raise forms.ValidationError('Wrong answer.')
