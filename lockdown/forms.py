from django import forms

from lockdown import settings


class BaseLockdownForm(forms.Form):
    def generate_token(self):
        """
        Generate a token which can be used to authenticate the user for future
        requests.
        
        """
        return True

    def authenticate(self, token_value):
        """
        Authenticate the user from a stored token value. If the ``token_value``
        is ``None``, then no token was retrieved.
         
        """
        return token_value is True

    def show_form(self):
        """
        Determine whether or not the form should be shown on locked pages.
        
        """
        return True


class LockdownForm(BaseLockdownForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def __init__(self, passwords=None, *args, **kwargs):
        super(LockdownForm, self).__init__(*args, **kwargs)
        if passwords is None:
            passwords = settings.PASSWORDS
        self.valid_passwords = passwords

    def clean_password(self):
        """
        Check that the password is valid.
        
        """
        value = self.cleaned_data.get('password')
        if not value in self.valid_passwords:
            raise forms.ValidationError('Incorrect password.')
        return value

    def generate_token(self):
        """
        Save the password as the authentication token.
        
        It's acceptable to store the password raw, as it is stored server-side
        in the user's session.
        
        """
        return self.cleaned_data['password']

    def authenticate(self, token_value):
        """
        Check that the password is valid.
        
        This allows for revoking of a user's preview rights by changing the
        valid passwords.
        
        """
        return token_value in self.valid_passwords

    def show_form(self):
        """
        Show the form if there are any valid passwords.
         
        """
        return bool(self.valid_passwords)
