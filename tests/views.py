from django.http import HttpResponse

from lockdown.decorators import lockdown


def aview(request):
    return HttpResponse('A view.')


@lockdown()
def lockedview(request):
    return HttpResponse('A locked view.')


@lockdown(passwords=('squirrel',))
def nutcracker(request):
    return HttpResponse('A locked view.')
