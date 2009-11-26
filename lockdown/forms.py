from django import forms

from lockdown import settings


class LockdownForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean_password(self):
        if self.cleaned_data['password'] in settings.PASSWORD:
            return self.cleaned_data['password']
        raise forms.ValidationError('Incorrect password.')
