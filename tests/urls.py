from django.conf.urls.defaults import *

urlpatterns = patterns(
    'tests.views',
    (r'^$', 'index'),
    (r'^a/view/$', 'aview'),
#    (r'^locked/view/$', 'lockedview'),
    )
