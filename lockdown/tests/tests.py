import datetime

from pkg_resources import parse_version

import django
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from lockdown import middleware, settings
from lockdown.forms import AuthForm


class LockdownTestCase(TestCase):

    """Base class for the other tests, setting up a proper test environment."""

    urls = 'lockdown.tests.urls'

    def setUp(self):
        """Basic setup for all tests."""
        self._old_pw = settings.PASSWORDS
        settings.PASSWORDS = ('letmein',)

        self._old_form = settings.FORM
        settings.FORM = 'lockdown.forms.LockdownForm'
        middleware._default_form = middleware.get_lockdown_form(settings.FORM)

    def tearDown(self):
        """Tearing down all settings made for the tests after running them."""
        settings.PASSWORDS = self._old_pw
        settings.FORM = self._old_form
        middleware._default_form = middleware.get_lockdown_form(settings.FORM)


class BaseTests(LockdownTestCase):

    """Base tests for lockdown functionality.

    These base tests are used for testing lockdowns decorator and middleware
    functionality.

    Subclasses should provide ``locked_url`` and ``locked_contents``
    attributes.
    """

    def test_lockdown_template_used(self):
        """Test if the login form template is used on locked pages."""
        response = self.client.get(self.locked_url)
        self.assertTemplateUsed(response, 'lockdown/form.html')

    def test_form_in_context(self):
        """Test if the login form contains a proper password field."""
        response = self.client.get(self.locked_url)
        form = response.context['form']
        self.failUnless('password' in form.fields)

    def test_global_disable(self):
        """Test that a page isn't locked when LOCKDOWN_ENABLED=False."""
        _old_enabled = settings.ENABLED
        settings.ENABLED = False
        try:
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)
        finally:
            settings.ENABLED = _old_enabled

    def test_url_exceptions(self):
        """Test that a page isn't locked when its URL is in the exception list.

        The excepted URLs are determinated by the
        LOCKDOWN_URL_EXCEPTIONS setting.
        """
        _old_url_exceptions = settings.URL_EXCEPTIONS
        settings.URL_EXCEPTIONS = (r'/view/$',)
        middleware._default_url_exceptions = \
            middleware.compile_url_exceptions(settings.URL_EXCEPTIONS)

        try:
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)
        finally:
            settings.URL_EXCEPTIONS = _old_url_exceptions
            middleware._default_url_exceptions = \
                middleware.compile_url_exceptions(settings.URL_EXCEPTIONS)

    def test_submit_password(self):
        """Test that access to locked content works with a correct password."""
        response = self.client.post(self.locked_url, {'password': 'letmein'},
                                    follow=True)
        self.assertEqual(response.content, self.locked_contents)

    def test_submit_wrong_password(self):
        """Test access to locked content is denied for wrong passwords."""
        response = self.client.post(self.locked_url, {'password': 'imacrook'})
        self.assertContains(response, 'Incorrect password.')

    def test_custom_form(self):
        """Test if access using a custom lockdown form works."""
        _old_form = settings.FORM
        settings.FORM = 'lockdown.tests.forms.CustomLockdownForm'
        middleware._default_form = middleware.get_lockdown_form(settings.FORM)

        try:
            response = self.client.post(self.locked_url, {'answer': '42'},
                                        follow=True)
            self.assertEqual(response.content, self.locked_contents)
        finally:
            settings.FORM = _old_form
            middleware._default_form = middleware.get_lockdown_form(
                settings.FORM)

    def test_invalid_custom_form(self):
        """Test that pointing to an invalid form properly produces an error."""
        # no form configured at all
        self.assertRaises(ImproperlyConfigured,
                          middleware.get_lockdown_form, None)
        # invalid module name in the configured form
        self.assertRaises(ImproperlyConfigured,
                          middleware.get_lockdown_form, 'invalidform')
        # not existing module for form
        self.assertRaises(ImproperlyConfigured,
                          middleware.get_lockdown_form, 'invalid.form')
        # existing module, but no form with that name in the module
        self.assertRaises(ImproperlyConfigured,
                          middleware.get_lockdown_form, 'lockdown.forms.foo')

    def test_locked_until(self):
        """Test locking until a certain date."""
        _old_until_date = settings.UNTIL_DATE
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

        try:
            settings.UNTIL_DATE = tomorrow
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

            settings.UNTIL_DATE = yesterday
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)
        finally:
            settings.UNTIL_DATE = _old_until_date

    def test_locked_after(self):
        """Test locking starting at a certain date."""
        _old_after_date = settings.AFTER_DATE
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

        try:
            settings.AFTER_DATE = yesterday
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

            settings.AFTER_DATE = tomorrow
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)
        finally:
            settings.AFTER_DATE = _old_after_date

    def test_locked_until_and_after(self):
        """Test locking until a certain date and starting at another date."""
        _old_until_date = settings.UNTIL_DATE
        _old_after_date = settings.AFTER_DATE
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

        try:
            settings.UNTIL_DATE = yesterday
            settings.AFTER_DATE = yesterday
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

            settings.UNTIL_DATE = tomorrow
            settings.AFTER_DATE = tomorrow
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

            settings.UNTIL_DATE = yesterday
            settings.AFTER_DATE = tomorrow
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)
        finally:
            settings.UNTIL_DATE = _old_until_date
            settings.AFTER_DATE = _old_after_date

    def test_missing_session_middleware(self):
        """Test behavior with missing session middleware.

        When the session middleware isn't present an ImproperlyConfigured error
        is expected.
        """
        middleware_remove = {
            'remove': [
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware'
            ]
        }

        if parse_version(django.get_version()) < parse_version('1.10'):
            with self.modify_settings(MIDDLEWARE_CLASSES=middleware_remove):
                self.assertRaises(ImproperlyConfigured,
                                  self.client.get,
                                  self.locked_url)
        else:
            with self.modify_settings(MIDDLEWARE=middleware_remove):
                self.assertRaises(ImproperlyConfigured,
                                  self.client.get,
                                  self.locked_url)


class DecoratorTests(BaseTests):

    """Tests for using lockdown via decorators."""

    locked_url = '/locked/view/'
    locked_contents = b'A locked view.'

    def test_overridden_password(self):
        """Test that locking works when overriding the password."""
        url = '/overridden/locked/view/'

        response = self.client.post(url, {'password': 'letmein'}, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        response = self.client.post(url, {'password': 'squirrel'}, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

    def test_overridden_url_exceptions(self):
        """Test that locking works when overriding the url exceptions."""
        url = '/locked/view/with/exception1/'
        response = self.client.post(url, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        url = '/locked/view/with/exception2/'
        response = self.client.post(url, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

    def test_overridden_until_date(self):
        """Test that locking works when overriding the until date."""
        url = '/locked/view/until/yesterday/'
        response = self.client.post(url, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

        url = '/locked/view/until/tomorrow/'
        response = self.client.post(url, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

    def test_overridden_after_date(self):
        """Test that locking works when overriding the after date."""
        url = '/locked/view/after/yesterday/'
        response = self.client.post(url, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        url = '/locked/view/after/tomorrow/'
        response = self.client.post(url, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

    def test_overridden_both_dates(self):
        """Test that locking works when overriding the after date."""
        url = '/locked/view/until/and/after/'
        response = self.client.post(url, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

    def test_overridden_extra_context(self):
        """Test that locking works when overriding the extra context."""
        url = '/locked/view/with/extra/context/'
        response = self.client.get(url)
        self.failUnless('foo' in response.context)


class MiddlewareTests(BaseTests):

    """Tests for using lockdown via its middleware."""

    locked_url = '/a/view/'
    locked_contents = b'A view.'

    def setUp(self):
        """Additional setup for middleware tests."""
        super(MiddlewareTests, self).setUp()
        if parse_version(django.get_version()) < parse_version('1.10'):
            self._old_middleware_classes = django_settings.MIDDLEWARE_CLASSES
            django_settings.MIDDLEWARE_CLASSES += (
                'lockdown.middleware.LockdownMiddleware',
            )
        else:
            self._old_middleware_classes = django_settings.MIDDLEWARE
            django_settings.MIDDLEWARE.append(
                'lockdown.middleware.LockdownMiddleware',
            )

    def tearDown(self):
        """Additional tear down for middleware tests."""
        if parse_version(django.get_version()) < parse_version('1.10'):
            django_settings.MIDDLEWARE_CLASSES = self._old_middleware_classes
        else:
            django_settings.MIDDLEWARE = self._old_middleware_classes
        super(MiddlewareTests, self).tearDown()


class AuthFormTests(LockdownTestCase):

    """Tests for using the auth form for previewing locked pages."""

    def test_using_form(self):
        """Test unauthorized access to locked page.

        Unauthorized access to a to locked page should show the auth form
        """
        url = '/auth/user/locked/view/'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        form = response.context['form']
        self.failUnless(isinstance(form, AuthForm))

    def add_user(self, username='test', password='pw', **kwargs):
        """Add a user used for testing the auth form."""
        from django.contrib.auth.models import User
        user = User(username=username, **kwargs)
        user.set_password(password)
        user.save()

    def test_user(self):
        """Test access to a locked page which requires authorization."""
        url = '/auth/user/locked/view/'
        self.add_user()

        # Incorrect password.
        post_data = {'username': 'test', 'password': 'bad'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        # Correct password.
        post_data = {'username': 'test', 'password': 'pw'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')

    def test_staff(self):
        """Test access to a locked page which requires a staff user."""
        url = '/auth/staff/locked/view/'
        self.add_user(username='user')
        self.add_user(username='staff', is_staff=True)

        # Non-staff member.
        post_data = {'username': 'user', 'password': 'pw'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        # Incorrect password.
        post_data = {'username': 'staff', 'password': 'bad'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        # Correct password.
        post_data = {'username': 'staff', 'password': 'pw'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')

    def test_superuser(self):
        """Test access to a locked page which requires a superuser."""
        url = '/auth/superuser/locked/view/'
        self.add_user(username='staff', is_staff=True)
        self.add_user(username='superuser', is_staff=True, is_superuser=True)

        # Non-superuser.
        post_data = {'username': 'staff', 'password': 'pw'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        # Incorrect password.
        post_data = {'username': 'superuser', 'password': 'bad'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        # Correct password.
        post_data = {'username': 'superuser', 'password': 'pw'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')


# Remove the BaseTests class from the module namespace, so it won't get picked
# up by unittest.
del BaseTests
