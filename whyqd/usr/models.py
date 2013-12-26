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

from datetime import datetime
import pytz
from taggit.managers import TaggableManager
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign, get_objects_for_user, get_perms

from whyqd.snippets.shrtn import surl, lurs

class User(AbstractUser):
    is_subscribed_to = models.DateTimeField(blank=True, null=True, default=datetime.now, verbose_name="Subscribed until")
    
    @property
    def get_logout_url(self):
        return reverse('account_logout')
    
    @property
    def is_subscribed(self):
        if self.is_subscribed_to > pytz.UTC.localize(datetime.now()):
            return True
        else:
            return False

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