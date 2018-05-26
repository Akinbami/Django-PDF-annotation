# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile, Notification

# Register your models here.
class NotificationModelAdmin(admin.ModelAdmin):
	list_display = ["__str__","from_user", "to_user", "pdf", "notification_type","is_read","is_reverted", "date"]
	list_filter = ["from_user", "notification_type", "date"]

	class Meta:
		model = Notification

admin.site.register(Profile)
admin.site.register(Notification,NotificationModelAdmin)
