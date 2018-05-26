# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone
from django.shortcuts import render

import reversion
from reversion.models import Version

from .forms import PDFForm
from .models import PDF
# Create your views here.

@login_required
def pdf_create(request):
	form = PDFForm(request.POST or None, request.FILES or None)
	print form
	if form.is_valid():
		with reversion.create_revision():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			reversion.set_user(request.user)
    		# reversion.set_comment(instance.comment)
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "pdf_form.html", context)

@login_required
def pdf_detail(request, slug=None):
	instance = get_object_or_404(PDF, slug=slug)
	# Load a queryset of versions for a specific model instance.
	versions = Version.objects.get_for_object(instance)
	# if instance.publish > timezone.now().date() or instance.draft:
	# 	if not request.user.is_staff or not request.user.is_superuser:
	# 		raise Http404
	share_string = quote_plus(instance.title)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id,
			}

	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"versions": versions,
	}
	return render(request, "pdf_detail.html", context)

# def preview(request, slug=None):
# 	file_path = settings.MEDIA_URL + /
# 	pdf_data = open("/path/to/my/image.pdf", "rb").read()
# 	return HttpResponse(pdf_data, mimetype="application/pdf")


@login_required
def pdf_update(request, slug=None):
	instance = get_object_or_404(PDF, slug=slug)
	form = PDFForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		with reversion.create_revision():
			instance = form.save(commit=False)
			instance.save()
			reversion.set_user(request.user)
    		# reversion.set_comment(instance.comment)
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "pdf_form.html", context)



class PDFContributorsToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("pdf")
        username = self.kwargs.get("username")

        obj = get_object_or_404(PDF, slug=slug)
        url_ = obj.get_absolute_url()
        user = get_object_or_404(User, username=username)

        if obj.user == self.request.user:
            if user in obj.contributor.all():
                obj.contributor.remove(user)
                print 'no'
            else:
                obj.contributor.add(user)
                user.profile.notify_invited(pdf=obj,invited_user=user)
                print 'yes'
        else:
            pass
        return url_

# def pdf_delete(request, slug=None):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404
# 	instance = get_object_or_404(Post, slug=slug)
# 	instance.delete()
# 	messages.success(request, "Successfully deleted")
# 	return redirect("posts:list")


