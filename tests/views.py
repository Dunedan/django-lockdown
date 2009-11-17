from django.http import HttpResponse

#from lockdown.decorators import lock

def index(request):
    return HttpResponse('The index view.')

def aview(request):
    return HttpResponse('A view.')

#@protect
#def lockedview(request):
#    return HttpResponse('A locked view.')
