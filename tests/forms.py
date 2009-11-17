from django import forms

class CustomLockdownForm(forms.Form):
    answer = forms.IntegerField()

    def clean_answer(self):
        if self.cleaned_data['answer'] == 42:
            return 42
        raise forms.ValidationError('Wrong answer.')
