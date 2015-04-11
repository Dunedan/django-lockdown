from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^a/view/$', views.a_view),
    url(r'^locked/view/$', views.locked_view),
    url(r'^overridden/locked/view/$', views.overridden_locked_view),
    url(r'^locked/view/with/exception/', views.locked_view_with_exception),
    url(r'^locked/view/with/exception2/', views.locked_view_with_exception),
    url(r'^auth/user/locked/view/$', views.user_locked_view),
    url(r'^auth/staff/locked/view/$', views.staff_locked_view),
    url(r'^auth/superuser/locked/view/$', views.superuser_locked_view),
]
