try:
    from django.conf.urls import patterns
except ImportError:
    from django.conf.urls.defaults import patterns  # Django <= 1.3

urlpatterns = patterns('lockdown.tests.views',
                       (r'^a/view/$', 'a_view'),
                       (r'^locked/view/$', 'locked_view'),
                       (r'^overridden/locked/view/$',
                        'overridden_locked_view'),
                       (r'^auth/user/locked/view/$', 'user_locked_view'),
                       (r'^auth/staff/locked/view/$', 'staff_locked_view'),
                       (r'^auth/superuser/locked/view/$',
                        'superuser_locked_view'),
                       )
