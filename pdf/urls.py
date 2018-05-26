from django.conf.urls import url
from django.contrib import admin

from .views import (
	pdf_create,
	pdf_detail,
	pdf_update,
	PDFContributorsToggle,
	)

urlpatterns = [
    url(r'^create/$', pdf_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', pdf_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', pdf_update, name='update'),
    url(r'^(?P<pdf>[\w-]+)/contibutor/(?P<username>[\w]+)$', PDFContributorsToggle.as_view(), name='contributor-toggle'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
