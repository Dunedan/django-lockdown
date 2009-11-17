from django.conf import settings

LOCKDOWN_URL_EXCEPTIONS = getattr(settings, 'LOCKDOWN_URL_EXCEPTIONS', ())
LOCKDOWN_PASSWORD = getattr(settings, 'LOCKDOWN_PASSWORD', None)
LOCKDOWN_FORM = getattr(settings, 'LOCKDOWN_FORM', None)
LOCKDOWN_SESSION_KEY = getattr(settings, 'LOCKDOWN_SESSION_KEY', 'lockdown-allow')
