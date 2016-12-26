from django import forms
from django.conf import settings as django_settings
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm

from lockdown import settings


class LockdownForm(forms.Form):

    """Defines a form to enter a password for accessing locked down content."""

    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def __init__(self, passwords=None, *args, **kwargs):
        """Initialize the form by setting the valid passwords."""
        super(LockdownForm, self).__init__(*args, **kwargs)
        if passwords is None:
            passwords = settings.PASSWORDS
        self.valid_passwords = passwords

    def clean_password(self):
        """Check that the password is valid."""
        value = self.cleaned_data.get('password')
        if value not in self.valid_passwords:
            raise forms.ValidationError('Incorrect password.')
        return value

    def generate_token(self):
        """Save the password as the authentication token.

        It's acceptable to store the password raw, as it is stored server-side
        in the user's session.
        """
        return self.cleaned_data['password']

    def authenticate(self, token_value):
        """Check that the password is valid.

        This allows for revoking of a user's preview rights by changing the
        valid passwords.
        """
        return token_value in self.valid_passwords

    def show_form(self):
        """Show the form if there are any valid passwords."""
        return bool(self.valid_passwords)


class AuthForm(AuthenticationForm):

    """Defines a form using Djangos authentication to access locked content.

    This form is a sample implementation of how to use a custom form to provide
    access to locked down content.
    """

    def __init__(self, staff_only=None, superusers_only=None, *args,
                 **kwargs):
        """Initialize the form by setting permissions needed for access."""
        super(AuthForm, self).__init__(*args, **kwargs)
        if staff_only is None:
            staff_only = getattr(django_settings,
                                 'LOCKDOWN_AUTHFORM_STAFF_ONLY', True)
        if superusers_only is None:
            superusers_only = getattr(django_settings,
                                      'LOCKDOWN_AUTHFORM_SUPERUSERS_ONLY',
                                      False)
        self.staff_only = staff_only
        self.superusers_only = superusers_only

    def clean(self):
        """When receiving the filled out form, check for valid access."""
        cleaned_data = super(AuthForm, self).clean()
        user = self.get_user()
        if self.staff_only and (not user or not user.is_staff):
            raise forms.ValidationError('Sorry, only staff are allowed.')
        if self.superusers_only and (not user or not user.is_superuser):
            raise forms.ValidationError('Sorry, only superusers are allowed.')
        return cleaned_data

    def generate_token(self):
        """Save the password as the authentication token.

        It's acceptable to store the password raw, as it is stored server-side
        in the user's session.
        """
        user = self.get_user()
        return '%s:%s' % (user.backend, user.pk)

    def authenticate(self, token_value):
        """Check that the password is valid.

        This allows for revoking of a user's preview rights by changing the
        valid passwords.
        """
        try:
            backend_path, user_id = token_value.split(':', 1)
        except (ValueError, AttributeError):
            return False
        backend = auth.load_backend(backend_path)
        return bool(backend.get_user(user_id))

    def show_form(self):
        """Determine if the form should be shown on locked pages."""
        return True
