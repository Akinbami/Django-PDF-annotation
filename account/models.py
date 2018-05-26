# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import post_save
from django.utils.html import escape


from pdf.models import PDF
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, default=1)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username


    def notify_upload(self, pdf):
        if self.user != pdf.user:
            Notification(notification_type=Notification.UPLOAD_UPDATE,
                         from_user=self.user,
                         to_user=pdf.user,
                         pdf=pdf).save()

    def notify_accepted_update(self, pdf):
        if self.user != pdf.user:
            Notification(notification_type=Notification.ACCEPTED_UPDATE,
                         from_user=self.user,
                         to_user=pdf.user,
                         pdf=pdf).save()

    def notify_rejected_update(self, pdf):
        if self.user != pdf.user:
            Notification(
                notification_type=Notification.REJECTED_UPDATE,
                from_user=self.user,
                to_user=pdf.user,
                pdf=pdf).save()

    def notify_invited(self, pdf,invited_user):
        if self.user != pdf.user or self.user != invited_user:
            Notification(notification_type=Notification.INVITE_USER,
                         from_user=pdf.user,
                         to_user=invited_user,
                         pdf=pdf).save()

    def notify_invited_acceptance(self,pdf, instance):
    	if not instance.is_reverted:
	        Notification(
	            notification_type=Notification.ACCEPTED_INVITATION,
	            from_user=instance.to_user,
	            to_user=instance.from_user,
	            pdf=pdf,
	            need_response=False).save()

    def notify_invited_rejected(self, pdf, instance):
    	if not instance.is_reverted:
	        Notification(
	            notification_type=Notification.REJECTED_INVITATION,
	            from_user=instance.to_user,
	            to_user=instance.from_user,
	            pdf=pdf,
	            need_response=False).save()


class Notification(models.Model):
    INVITE_USER = 'IU'
    ACCEPTED_INVITATION = 'AI'
    REJECTED_INVITATION = 'RI'
    ACCEPTED_UPDATE = 'AU'
    REJECTED_UPDATE = 'RU'
    UPLOAD_UPDATE = 'UU'
    NOTIFICATION_TYPES = (
        (INVITE_USER, 'Invite'),
        (ACCEPTED_INVITATION, 'Accepted Invitation'),
        (ACCEPTED_UPDATE, 'Accepted Update'),
        (UPLOAD_UPDATE, 'Uploaded Update'),
        )

    _INVITE_USER = '<a href="/{0}/">{1}</a> invites you for collaboration : {3}'  # noqa: E501
    _ACCEPTED_INVITATION = '<a href="/{0}/">{1}</a> accepted your initation: {3}'  # noqa: E501
    _REJECTED_INVITATION = '<a href="/{0}/">{1}</a> rejected your initation: {3}'  # noqa: E501
    _ACCEPTED_UPDATE = '<a href="/{0}/">{1}</a> accepted your update: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _REJECTED_UPDATE = '<a href="/{0}/">{1}</a> rejected your update: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _UPLOAD_UPDATE = '<a href="/{0}/">{1}</a> Upload an update: <a href="/questions/{2}/">{3}</a>'  # noqa: E501

    
    from_user = models.ForeignKey(User, related_name='notification_from')
    to_user = models.ForeignKey(User, related_name='notification_to')
    date = models.DateTimeField(auto_now_add=True)
    pdf = models.ForeignKey(PDF, null=True, blank=True)
    notification_type = models.CharField(max_length=2,
                                         choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    is_reverted = models.BooleanField(default=False)
    need_response =  models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.INVITE_USER:
            return self._INVITE_USER.format(
                self.pdf.slug,
                self.from_user.username,
                self.pdf.pk,
                self.get_summary(self.pdf.comment)
                )
        elif self.notification_type == self.ACCEPTED_INVITATION:
            return self._ACCEPTED_INVITATION.format(
                escape(self.pdf.slug),
                escape(self.from_user),
                self.pdf.pk,
                escape(self.get_summary(self.pdf.comment))
                )

        elif self.notification_type == self.REJECTED_INVITATION:
            return self._REJECTED_INVITATION.format(
                escape(self.pdf.slug),
                escape(self.from_user),
                self.pdf.pk,
                escape(self.get_summary(self.pdf.comment))
                )
        elif self.notification_type == self.ACCEPTED_UPDATE:
            return self._ACCEPTED_UPDATE.format(
                escape(self.from_user.username),
                escape(self.from_user),
                self.pdf.pk,
                escape(self.get_summary(self.pdf.comment))
                )
        elif self.notification_type == self.REJECTED_UPDATE:
            return self._REJECTED_UPDATE.format(
                escape(self.from_user.username),
                escape(self.from_user),
                self.pdf.pk,
                escape(self.get_summary(self.pdf.title))
                )
        elif self.notification_type == self.UPLOAD_UPDATE:
            return self._UPLOAD_UPDATE.format(
                escape(self.from_user.username),
                escape(self.from_user),
                self.answer.pdf.pk,
                escape(self.get_summary(self.pdf.comment))
                )

        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)