from django.http import HttpResponse

from lockdown.decorators import lockdown

def index(request):
    return HttpResponse('The index view.')

def aview(request):
    return HttpResponse('A view.')

@lockdown
def lockedview(request):
    return HttpResponse('A locked view.')
