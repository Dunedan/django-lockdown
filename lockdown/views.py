"""
views for django-markitup

Time-stamp: <2009-11-06 02:26:59 carljm views.py>

"""
from django.shortcuts import render_to_response
from markitup import settings

from markitup.markup import filter_func

def apply_filter(request):
    markup = filter_func(request.POST.get('data', ''))
    return render_to_response( 'markitup/preview.html',
                              {'preview':markup,
                               'MEDIA_URL': settings.MARKITUP_MEDIA_URL.rstrip('/')})
