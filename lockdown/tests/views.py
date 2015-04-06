from django.http import HttpResponse

from lockdown.decorators import lockdown
from lockdown.forms import AuthForm


def a_view(request):
    """Regular unlocked view"""
    return HttpResponse('A view.')


@lockdown()
def locked_view(request):
    """View, locked by the default lockdown decorator"""
    return HttpResponse('A locked view.')


@lockdown(passwords=('squirrel',))
def overridden_locked_view(request):
    """View, locked by the decorator with a custom password"""
    return HttpResponse('A locked view.')


@lockdown(form=AuthForm, staff_only=False)
def user_locked_view(request):
    """View, locked by the decorator with access for known users only"""
    return HttpResponse('A locked view.')


@lockdown(form=AuthForm)
def staff_locked_view(request):
    """View, locked by the decorator with access for staff users only"""
    return HttpResponse('A locked view.')


@lockdown(form=AuthForm, superusers_only=True)
def superuser_locked_view(request):
    """View, locked by the decorator with access for superusers only"""
    return HttpResponse('A locked view.')
