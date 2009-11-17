from django.test import TestCase, Client
from django.conf import settings as django_settings

from lockdown import settings
from lockdown.middleware import _compile_url_exceptions, _get_lockdown_form

class DecoratorTests(TestCase):
    _url = '/locked/view/'
    _contents = 'A locked view.'
    
    def setUp(self):
        self._old_pw = settings.LOCKDOWN_PASSWORD
        settings.LOCKDOWN_PASSWORD = 'letmein'
        _get_lockdown_form()
        self.client = Client()

    def tearDown(self):
        settings.LOCKDOWN_PASSWORD = self._old_pw

    def test_lockdown_template_used(self):
        response = self.client.get(self._url)
        template_name = ''
        if response.template:
            try:
                template_name = response.template.name
            except AttributeError:
                template_name = response.template[0].name
        self.assertEquals(template_name, 'lockdown/form.html')

    def test_form_in_context(self):
        response = self.client.get(self._url)
        form = response.context['form']
        self.failUnless('password' in form.fields)

    def test_url_exceptions(self):
        _old_url_exceptions = settings.LOCKDOWN_URL_EXCEPTIONS
        settings.LOCKDOWN_URL_EXCEPTIONS = (r'/view/$',)
        _compile_url_exceptions()

        response = self.client.get(self._url)
        self.assertContains(response, self._contents)

        settings.LOCKDOWN_URL_EXCEPTIONS = _old_url_exceptions
        _compile_url_exceptions()
        
    def test_submit_password(self):
        response = self.client.post(self._url, {'password': 'letmein'},
                                    follow=True)
        self.assertContains(response, self._contents)

    def test_submit_wrong_password(self):
        response = self.client.post(self._url, {'password': 'imacrook'})
        self.assertContains(response, 'Incorrect password.')

    def test_custom_form(self):
        _old_form = settings.LOCKDOWN_FORM
        settings.LOCKDOWN_FORM = 'tests.forms.CustomLockdownForm'
        _get_lockdown_form()
        
        response = self.client.post(self._url, {'answer': '42'},
                                    follow=True)
        self.assertContains(response, self._contents)
                                    
        settings.LOCKDOWN_FORM = _old_form
        _get_lockdown_form()
    

class MiddlewareTests(DecoratorTests):
    _url = '/a/view/'
    _contents = 'A view.'
    
    def setUp(self):
        self._old_middleware_classes = django_settings.MIDDLEWARE_CLASSES
        django_settings.MIDDLEWARE_CLASSES += ('lockdown.middleware.LockdownMiddleware',)
        super(MiddlewareTests, self).setUp()

    def tearDown(self):
        django_settings.MIDDLEWARE_CLASSES = self._old_middleware_classes
        super(MiddlewareTests, self).tearDown()
