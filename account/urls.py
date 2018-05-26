from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
	url(r'^$', home, name='home'),
	url(r'^register/$', register_view, name='register'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^ajax/get_invites/', get_invites, name='get_invites'),
    url(r'^notifications/$', notifications, name='notifications'),
    url(r'^notifications/last/$', last_notifications, name='last_notifications'),
    url(r'^notifications/check/$', check_notifications, name='check_notifications'),
    url(r'^accept_invitation/(?P<id>\d+)/$', accept_invitation, name='invite_accept'),
    url(r'^reject_invitation/(?P<id>\d+)/$', reject_invitation, name='invite_reject'),  
    # url(r'^team/create$', create_team, name='team'),
]
