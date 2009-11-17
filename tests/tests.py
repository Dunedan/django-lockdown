from django.test import TestCase, Client
from django.conf import settings as django_settings

from lockdown import settings
from lockdown.middleware import _compile_url_exceptions, _get_lockdown_form

class MiddlewareTests(TestCase):
    def setUp(self):
        self._old_middleware_classes = django_settings.MIDDLEWARE_CLASSES
        django_settings.MIDDLEWARE_CLASSES += ('lockdown.middleware.LockdownMiddleware',)
        self._old_pw = settings.LOCKDOWN_PASSWORD
        settings.LOCKDOWN_PASSWORD = 'letmein'
        _get_lockdown_form()
        self.client = Client()

    def tearDown(self):
        django_settings.MIDDLEWARE_CLASSES = self._old_middleware_classes
        settings.LOCKDOWN_PASSWORD = self._old_pw

    def test_lockdown_template_used(self):
        response = self.client.get('/')
        template_name = ''
        if response.template:
            try:
                template_name = response.template.name
            except AttributeError:
                template_name = response.template[0].name
        self.assertEquals(template_name, 'lockdown/form.html')

    def test_form_in_context(self):
        response = self.client.get('/')
        form = response.context['form']
        self.failUnless('password' in form.fields)

    def test_url_exceptions(self):
        _old_url_exceptions = settings.LOCKDOWN_URL_EXCEPTIONS
        settings.LOCKDOWN_URL_EXCEPTIONS = (r'^/a/',)
        _compile_url_exceptions()

        response = self.client.get('/a/view/')
        self.assertContains(response, 'A view.')

        settings.LOCKDOWN_URL_EXCEPTIONS = _old_url_exceptions
        _compile_url_exceptions()
        
    def test_submit_password(self):

        response = self.client.post('/', {'password': 'letmein'}, follow=True)
        self.assertContains(response, 'The index view.')
