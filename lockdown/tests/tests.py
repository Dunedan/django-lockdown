# pylint: disable=invalid-name,too-many-public-methods

import datetime

from django.conf import settings as django_settings
from django.contrib.auth.models import \
    User  # pylint: disable=imported-auth-user
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from lockdown import middleware
from lockdown.forms import AuthForm
from lockdown.tests.views import a_view


class BaseTests(TestCase):
    """Base tests for lockdown functionality.

    These base tests are used for testing lockdowns decorator and middleware
    functionality.

    Subclasses should provide ``locked_url`` and ``locked_contents``
    attributes.
    """

    locked_url = '/locked/view/'
    locked_contents = b'A locked view.'

    def test_lockdown_template_used(self):
        """Test if the login form template is used on locked pages."""
        response = self.client.get(self.locked_url)
        self.assertTemplateUsed(response, 'lockdown/form.html')

    @override_settings(LOCKDOWN_PASSWORDS=('letmein',))
    def test_form_in_context(self):
        """Test if the login form contains a proper password field."""
        response = self.client.get(self.locked_url)
        form = response.context['form']
        self.assertIn('password', form.fields)

    @override_settings(LOCKDOWN_ENABLED=False)
    def test_global_disable(self):
        """Test that a page isn't locked when LOCKDOWN_ENABLED=False."""
        response = self.client.get(self.locked_url)
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_URL_EXCEPTIONS=(r'/view/$',))
    def test_url_exceptions(self):
        """Test that a page isn't locked when its URL is in the exception list.

        The excepted URLs are determined by the LOCKDOWN_URL_EXCEPTIONS
        setting.
        """
        response = self.client.get(self.locked_url)
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.1'])
    def test_remote_addr_exc_lock(self):
        """Test that a page is locked when client IP is not in exception list.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS setting.
        """
        response = self.client.get(self.locked_url,
                                   REMOTE_ADDR='192.168.0.100')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.1'])
    def test_remote_addr_exc_unlock(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS setting.
        """
        response = self.client.get(self.locked_url, REMOTE_ADDR='192.168.0.1')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['fd::1'])
    def test_remote_addr_exc_unlock_ipv6(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS setting.
        """
        response = self.client.get(
            self.locked_url,
            REMOTE_ADDR='fd:0000:0000:0000:0000:0000:0000:0001')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.0/24'])
    def test_remote_addr_exc_unlock_subnet(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS setting.
        """
        response = self.client.get(self.locked_url, REMOTE_ADDR='192.168.0.1')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['fd::0/80'])
    def test_remote_addr_exc_unlock_ipv6_subnet(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS setting.
        """
        response = self.client.get(
            self.locked_url,
            REMOTE_ADDR='fd:0000:0000:0000:0000:0000:0000:0001')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.1'],
                       LOCKDOWN_TRUSTED_PROXIES=['127.0.0.1'])
    def test_untrusted_proxy_lock(self):
        """Test that a page is locked when proxy is not trusted.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(self.locked_url,
                                   REMOTE_ADDR='172.17.0.1',
                                   HTTP_X_FORWARDED_FOR='192.168.0.1')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['fd::2'],
                       LOCKDOWN_TRUSTED_PROXIES=['fd::1'])
    def test_untrusted_proxy_lock_ipv6(self):
        """Test that a page is locked when proxy is not trusted.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(
            self.locked_url, REMOTE_ADDR='2001:db8::ff00:42:8329',
            HTTP_X_FORWARDED_FOR='fd:0000:0000:0000:0000:0000:0000:0001')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.0/24'],
                       LOCKDOWN_TRUSTED_PROXIES=['127.0.0.0/24'])
    def test_untrusted_proxy_lock_subnet(self):
        """Test that a page is locked when proxy is not trusted.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(self.locked_url,
                                   REMOTE_ADDR='172.17.0.1',
                                   HTTP_X_FORWARDED_FOR='192.168.0.1')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['fd::2'],
                       LOCKDOWN_TRUSTED_PROXIES=['fd::1'])
    def test_untrusted_proxy_lock_ipv6_subnet(self):
        """Test that a page is locked when proxy is not trusted.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(
            self.locked_url, REMOTE_ADDR='2001:db8::ff00:42:8329',
            HTTP_X_FORWARDED_FOR='fd:0000:0000:0000:0000:0000:0000:0001')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.1'])
    def test_no_trusted_proxy_lock(self):
        """Test that a page is locked when x-forwarded-for is used w/o proxies.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(self.locked_url,
                                   REMOTE_ADDR='10.0.0.1',
                                   HTTP_X_FORWARDED_FOR='192.168.0.1')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['fd::0/80'])
    def test_no_trusted_proxy_lock_ipv6(self):
        """Test that a page is locked when x-forwarded-for is used w/o proxies.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(
            self.locked_url,
            REMOTE_ADDR='2001:db8::ff00:42:8329',
            HTTP_X_FORWARDED_FOR='fd:0000:0000:0000:0000:0000:0000:0001')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.0/24'])
    def test_no_trusted_proxy_lock_subnet(self):
        """Test that a page is locked when x-forwarded-for is used w/o proxies.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(self.locked_url,
                                   REMOTE_ADDR='10.0.0.1',
                                   HTTP_X_FORWARDED_FOR='192.168.0.100')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['fd::0/80'])
    def test_no_trusted_proxy_lock_ipv6_subnet(self):
        """Test that a page is locked when x-forwarded-for is used w/o proxies.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(
            self.locked_url,
            REMOTE_ADDR='fe::1',
            HTTP_X_FORWARDED_FOR='fd::2')
        self.assertNotEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.1'],
                       LOCKDOWN_TRUSTED_PROXIES=['10.0.0.1'])
    def test_trusted_proxy_unlock(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(self.locked_url,
                                   REMOTE_ADDR='10.0.0.1',
                                   HTTP_X_FORWARDED_FOR='192.168.0.1')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=[
            'fd:0000:0000:0000:0000:0000:0000:0001'],
        LOCKDOWN_TRUSTED_PROXIES=['fd:0000:0000:0000:0000:0000:0000:0002'])
    def test_trusted_proxy_unlock_ipv6(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-addresses are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(
            self.locked_url,
            REMOTE_ADDR='fd:0000:0000:0000:0000:0000:0000:0002',
            HTTP_X_FORWARDED_FOR='fd:0000:0000:0000:0000:0000:0000:0001')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['192.168.0.0/24'],
                       LOCKDOWN_TRUSTED_PROXIES=['127.0.0.0/24'])
    def test_trusted_proxy_unlock_subnet(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(self.locked_url,
                                   REMOTE_ADDR='127.0.0.1',
                                   HTTP_X_FORWARDED_FOR='192.168.0.1')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_REMOTE_ADDR_EXCEPTIONS=['fd::0/80'],
                       LOCKDOWN_TRUSTED_PROXIES=['fe::0/80'])
    def test_trusted_proxy_unlock_ipv6_subnet(self):
        """Test that a page isn't locked when client IP is in exception list.

        The excepted IP-subnets are determined by the
        LOCKDOWN_REMOTE_ADDR_EXCEPTIONS and TRUSTED_PROXIES settings.
        """
        response = self.client.get(
            self.locked_url,
            REMOTE_ADDR='fe::2',
            HTTP_X_FORWARDED_FOR='fd::1')
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_PASSWORDS=('letmein',))
    def test_submit_password(self):
        """Test that access to locked content works with a correct password."""
        response = self.client.post(self.locked_url, {'password': 'letmein'},
                                    follow=True)
        self.assertEqual(response.content, self.locked_contents)

    @override_settings(LOCKDOWN_PASSWORDS=('letmein',))
    def test_submit_wrong_password(self):
        """Test access to locked content is denied for wrong passwords."""
        response = self.client.post(self.locked_url, {'password': 'imacrook'})
        self.assertContains(response, 'Incorrect password.')

    @override_settings(LOCKDOWN_FORM='lockdown.tests.forms.CustomLockdownForm')
    def test_custom_form(self):
        """Test if access using a custom lockdown form works."""
        response = self.client.post(self.locked_url, {'answer': '42'},
                                    follow=True)
        self.assertEqual(response.content, self.locked_contents)

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
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

        with self.settings(LOCKDOWN_UNTIL_DATE=tomorrow):
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

        with self.settings(LOCKDOWN_UNTIL_DATE=yesterday):
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)

    def test_locked_after(self):
        """Test locking starting at a certain date."""
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

        with self.settings(LOCKDOWN_AFTER_DATE=yesterday):
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

        with self.settings(LOCKDOWN_AFTER_DATE=tomorrow):
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)

    def test_locked_until_and_after(self):
        """Test locking until a certain date and starting at another date."""
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

        with self.settings(LOCKDOWN_UNTIL_DATE=yesterday,
                           LOCKDOWN_AFTER_DATE=yesterday):
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

        with self.settings(LOCKDOWN_UNTIL_DATE=tomorrow,
                           LOCKDOWN_AFTER_DATE=tomorrow):
            response = self.client.get(self.locked_url)
            self.assertTemplateUsed(response, 'lockdown/form.html')

        with self.settings(LOCKDOWN_UNTIL_DATE=yesterday,
                           LOCKDOWN_AFTER_DATE=tomorrow):
            response = self.client.get(self.locked_url)
            self.assertEqual(response.content, self.locked_contents)

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

        with self.modify_settings(MIDDLEWARE=middleware_remove):
            self.assertRaises(ImproperlyConfigured,
                              self.client.get,
                              self.locked_url)


class DecoratorTests(BaseTests):
    """Tests for using lockdown via decorators."""

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

    def test_overridden_ip_exceptions(self):
        """Test that locking works with overwritten remote_addr exceptions."""
        url = '/locked/view/with/ip_exception/'
        response = self.client.post(url, REMOTE_ADDR='192.168.0.100',
                                    follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        url = '/locked/view/with/ip_exception/'
        response = self.client.post(url, REMOTE_ADDR='192.168.0.1',
                                    follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

    def test_overridden_ip_exceptions_ipv6(self):
        """Test that locking works with overwritten remote_addr exceptions."""
        url = '/locked/view/with/ip_exception_ipv6/'
        response = self.client.post(
            url, REMOTE_ADDR='fd:0000:0000:0000:0000:0000:0000:0002',
            follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        url = '/locked/view/with/ip_exception_ipv6/'
        response = self.client.post(
            url, REMOTE_ADDR='fd:0000:0000:0000:0000:0000:0000:0001',
            follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

    def test_overridden_ip_exceptions_subnet(self):
        """Test that locking works with overwritten remote_addr exceptions."""
        url = '/locked/view/with/ip_exception_subnet/'
        response = self.client.post(url, REMOTE_ADDR='172.0.0.1',
                                    follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        url = '/locked/view/with/ip_exception_subnet/'
        response = self.client.post(url, REMOTE_ADDR='192.168.0.1',
                                    follow=True)
        self.assertTemplateNotUsed(response, 'lockdown/form.html')
        self.assertEqual(response.content, self.locked_contents)

    def test_overridden_ip_exceptions_subnet_ipv6(self):
        """Test that locking works with overwritten remote_addr exceptions."""
        url = '/locked/view/with/ip_exception_ipv6_subnet/'
        response = self.client.post(url, REMOTE_ADDR='2001:db8::ff00:42:8329',
                                    follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        url = '/locked/view/with/ip_exception_ipv6_subnet/'
        response = self.client.post(url, REMOTE_ADDR='fd::1',
                                    follow=True)
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
        self.assertIn('foo', response.context)


class MiddlewareTests(BaseTests):
    """Tests for using lockdown via its middleware."""

    locked_url = '/a/view/'
    locked_contents = b'A view.'

    def setUp(self):
        """Additional setup for middleware tests."""
        super().setUp()
        self._old_middleware_classes = django_settings.MIDDLEWARE
        django_settings.MIDDLEWARE.append(
            'lockdown.middleware.LockdownMiddleware',
        )

    @override_settings(LOCKDOWN_VIEW_EXCEPTIONS=[a_view])
    def test_view_exceptions(self):
        """Test that a page isn't locked when its view whitelisted.

        The excepted URLs are determined by the
        LOCKDOWN_VIEW_EXCEPTIONS setting.
        """
        response = self.client.get(self.locked_url)
        self.assertEqual(response.content, self.locked_contents)

    def tearDown(self):
        """Additional tear down for middleware tests."""
        django_settings.MIDDLEWARE = self._old_middleware_classes
        super().tearDown()


class AuthFormTests(TestCase):
    """Tests for using the auth form for previewing locked pages."""

    def test_using_form(self):
        """Test unauthorized access to locked page.

        Unauthorized access to a to locked page should show the auth form
        """
        url = '/auth/user/locked/view/'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'lockdown/form.html')

        form = response.context['form']
        self.assertTrue(isinstance(form, AuthForm))

    def add_user(self, username='test', password='pw', **kwargs):  # nosec
        """Add a user used for testing the auth form."""
        user = User(username=username, **kwargs)
        user.set_password(password)
        user.save()

    def test_inactive_user(self):
        """Test access to a locked page with an inactive user."""
        url = '/auth/user/locked/view/'
        self.add_user(is_active=False)

        post_data = {'username': 'test', 'password': 'pw'}
        response = self.client.post(url, post_data, follow=True)
        self.assertTemplateUsed(response, 'lockdown/form.html')

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
