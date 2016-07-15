import datetime

from django.http import HttpResponse

from lockdown.decorators import lockdown
from lockdown.forms import AuthForm

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)
TOMORROW = datetime.datetime.now() + datetime.timedelta(days=1)


def a_view(request):
    """Regular unlocked view."""
    return HttpResponse('A view.')


@lockdown()
def locked_view(request):
    """View, locked by the default lockdown decorator."""
    return HttpResponse('A locked view.')


@lockdown(passwords=('squirrel',))
def overridden_locked_view(request):
    """View, locked by the decorator with a custom password."""
    return HttpResponse('A locked view.')


@lockdown(url_exceptions=(r'^/locked/view/with/exception2/',))
def locked_view_with_exception(request):
    """View, locked by the decorator with url exceptions."""
    return HttpResponse('A locked view.')


@lockdown(extra_context={'foo': 'bar'})
def locked_view_with_extra_context(request):
    """View, locked by the decorator with extra context."""
    return HttpResponse('A locked view.')


@lockdown(until_date=YESTERDAY)
def locked_view_until_yesterday(request):
    """View, locked till yesterday."""
    return HttpResponse('A locked view.')


@lockdown(until_date=TOMORROW)
def locked_view_until_tomorrow(request):
    """View, locked till tomorrow."""
    return HttpResponse('A locked view.')


@lockdown(after_date=YESTERDAY)
def locked_view_after_yesterday(request):
    """View, locked since yesterday."""
    return HttpResponse('A locked view.')


@lockdown(after_date=TOMORROW)
def locked_view_after_tomorrow(request):
    """View, locked starting from tomorrow."""
    return HttpResponse('A locked view.')


@lockdown(until_date=YESTERDAY, after_date=TOMORROW)
def locked_view_until_and_after(request):
    """View, only not looked between yesterday and tomorrow."""
    return HttpResponse('A locked view.')


@lockdown(form=AuthForm, staff_only=False)
def user_locked_view(request):
    """View, locked by the decorator with access for known users only."""
    return HttpResponse('A locked view.')


@lockdown(form=AuthForm)
def staff_locked_view(request):
    """View, locked by the decorator with access for staff users only."""
    return HttpResponse('A locked view.')


@lockdown(form=AuthForm, superusers_only=True)
def superuser_locked_view(request):
    """View, locked by the decorator with access for superusers only."""
    return HttpResponse('A locked view.')
