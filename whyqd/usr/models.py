from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.query import QuerySet
from django.db.models import Q
# Allowing generic relations - https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/
#         content_type = models.ForeignKey(ContentType)
#         object_id = models.PositiveIntegerField()
#         content_object = generic.GenericForeignKey("content_type", "object_id")
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django_facebook.models import FacebookModel

from datetime import datetime
import pytz
from taggit.managers import TaggableManager
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign, get_objects_for_user, get_perms
import hashlib

from whyqd.snippets.shrtn import surl, lurs

class User(AbstractUser, FacebookModel):
    is_subscribed_to = models.DateTimeField(blank=True, null=True, default=pytz.UTC.localize(datetime.now()), verbose_name="Subscribed until")
    state = models.CharField(max_length=255, blank=True, null=True)
    
    @property
    def get_logout_url(self):
        return reverse('account_logout')
    
    @property
    def is_subscribed(self):
        if self.is_subscribed_to > pytz.UTC.localize(datetime.now()):
            return True
        else:
            return False
'''    
    @property
    def account_verified(self):
        if self.is_authenticated:
            result = EmailAddress.objects.filter(email=self.email)
            if len(result):
                return result[0].verified
        return False
    
    @property
    def image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=20&height=20".format(fb_uid[0].uid)
        else:
            return "http://www.gravatar.com/avatar/{}?s=20".format(hashlib.md5(self.email).hexdigest())
'''
#########################################################################################################################################
# Model for storing saved working spaces with any type of wiqi for creating projects / analytics / charts / etc.
#########################################################################################################################################
"""
class StashStack(models.Model):
    stash_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_stash", null=True)
    stash_object_id = models.PositiveIntegerField(null=True)
    stash = generic.GenericForeignKey("stash_content_type", "stash_object_id")
    
class Stash(models.Model):
    name = models.CharField(max_length=250, blank=True)
    tags = TaggableManager(blank=True, verbose_name="Tags")
    is_active = models.BooleanField(default=True)
    is_latest = models.BooleanField(default=True)
    stashstack = models.ManyToManyField(StashStack)
    users = models.ManyToManyField(User)
"""