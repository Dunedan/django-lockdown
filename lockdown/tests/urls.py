from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^a/view/$', views.a_view),
    url(r'^locked/view/$', views.locked_view),
    url(r'^overridden/locked/view/$', views.overridden_locked_view),
    url(r'^locked/view/with/exception1/', views.locked_view_with_exception),
    url(r'^locked/view/with/exception2/', views.locked_view_with_exception),
    url(r'^locked/view/with/extra/context/',
        views.locked_view_with_extra_context),
    url(r'^locked/view/until/yesterday/', views.locked_view_until_yesterday),
    url(r'^locked/view/until/tomorrow/', views.locked_view_until_tomorrow),
    url(r'^locked/view/after/yesterday/', views.locked_view_after_yesterday),
    url(r'^locked/view/after/tomorrow/', views.locked_view_after_tomorrow),
    url(r'^locked/view/until/and/after/', views.locked_view_until_and_after),
    url(r'^auth/user/locked/view/$', views.user_locked_view),
    url(r'^auth/staff/locked/view/$', views.staff_locked_view),
    url(r'^auth/superuser/locked/view/$', views.superuser_locked_view),
]
