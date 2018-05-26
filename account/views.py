from __future__ import unicode_literals

import json


from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render,render_to_response
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from .decorators import ajax_required


from pdf.models import PDF
from .forms import *
from .models import Notification


# Create your views here.

@login_required
def home(request):
	today = timezone.now().date()
	user = get_object_or_404(User, username=request.user)
	notifications = Notification.objects.filter(to_user=user).filter(is_read=False)
	queryset_list = PDF.objects.filter(user=user).order_by("-timestamp")
	queryset_list2 = PDF.objects.filter(contributor__id=user.id).order_by("-timestamp")
	# if request.user.is_staff or request.user.is_superuser:
	# 	queryset_list = PDF.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
        'user': user,
        "object_list": queryset,
        "object_list2": queryset_list2,
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
		"num_notifications": notifications.count()
		}
	return render(request, 'index.html',  context)


def login_view(request):
    print "hello"
    if request.user.is_authenticated():
        return redirect("/")
    print(request.user.is_authenticated())
    # next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    print form
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        # if next:
        #     return redirect(next)
        return redirect("/")

    context = {
    	"form":form,
    	"title": title
    	}

    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def register_view(request):
    print "hello"
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Register"
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "register.html", context)

def get_invites(request):
	# print "hello"
	pdf = None
	if request.method == "GET":
		search_text = request.GET.get('username', '')
		pdf = request.GET.get('pdf')
		print search_text
	else:
		search_text = ''

	users = None
	if len(search_text)>0:
		users = User.objects.filter(username__contains = search_text )
		print users
		print pdf

	context = {
		'users':users,
		'pdf': pdf,
	}
	return render_to_response('invites.html', context)

def invite(request):
    if request.is_ajax():
        user = get_object_or_404(User,username=username)
        pdf = get_object_or_404(PDF, title=title)
        if user and pdf:
        	pdf.contributors.add(user)
        	title = "Unshare"
        # for user in users:
        #     user_json = {}
        #     user_json['username'] = user.username
        #     user_json['email'] = user.email
        #     results.append(user_json)
        data = json.dumps(title)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def accept_invitation(request, id=None):
	instance = get_object_or_404(Notification, id=id)
	user = instance.from_user
	obj = instance.pdf
	if instance:
		instance.is_read = True
		user.profile.notify_invited_acceptance(instance=instance,pdf=obj)
		instance.is_reverted = True
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect('/')
	return HttpResponseRedirect('/')
	
@login_required
def reject_invitation(request, id=None):
	instance = get_object_or_404(Notification, id=id)
	user = instance.from_user
	obj = instance.pdf
	if instance:
		instance.is_read = True
		user.profile.notify_invited_rejected(instance=instance,pdf=obj)
		instance.is_reverted = True
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect('/')
	return HttpResponseRedirect('/')

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True  # pragma: no cover
        notification.save()  # pragma: no cover
    context = {'notifications': notifications}
    return render(request, 'notifications.html',context)


@login_required
@ajax_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False)[:5]
    for notification in notifications:
        notification.is_read = True  # pragma: no cover
        notification.save()  # pragma: no cover

    return render(request,
                  'last_notifications.html',
                  {'notifications': notifications})


@login_required
@ajax_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False)[:5]
    return HttpResponse(len(notifications))

