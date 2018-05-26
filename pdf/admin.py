# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin
import reversion


# Register your models here.
from .models import PDF

@admin.register(PDF)
class PDFModelAdmin(VersionAdmin):
	list_display = ["title", "file", "timestamp"]
	list_display_links = ["title"]
	history_latest_first = True
	# list_editable = ["title"]
	# list_filter = ["updated", "timestamp"]

	search_fields = ["title"]
	class Meta:
		model = PDF


# reversion.register(PDFModelAdmin)