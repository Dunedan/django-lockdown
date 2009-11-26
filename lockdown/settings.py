from django.conf import settings

URL_EXCEPTIONS = getattr(settings, 'LOCKDOWN_URL_EXCEPTIONS', ())
PASSWORD = getattr(settings, 'LOCKDOWN_PASSWORD', None)
FORM = getattr(settings, 'LOCKDOWN_FORM', 'lockdown.forms.LockdownForm')
SESSION_KEY = getattr(settings, 'LOCKDOWN_SESSION_KEY', 'lockdown-allow')
