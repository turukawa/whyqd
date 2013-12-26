"""
Wiqi database schema
-------------------------------

Abstract classes:

        Wiqi:
                    is_live_from
                    is_live_to
                    is_active
                    is_protected
                    is_private
                    is_searchable
                    is_deleted
                    tags
                    base (generic foreign key)
                    forked (generic foreign key)
                    merged (generic foreign key)
        WiqiStack:
                    title
                    creator
                    creator_ip
                    created_on
                    licence
                    reverted_from (generic foreign key)
                    wiqi (generic foreign key)

Derived classes:
        
        Components:
                Wiqi -> Component(WiqiStack)
"""

from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.query import QuerySet
from django.db.models import Q
# Allowing generic relations - https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/
#         content_type = models.ForeignKey(ContentType)
#         object_id = models.PositiveIntegerField()
#         content_object = generic.GenericForeignKey("content_type", "object_id")
from django.conf import settings
from django.template.defaultfilters import slugify

from datetime import datetime
import pytz
import json
# Google Diff Match Patch library
# http://code.google.com/p/google-diff-match-patch
from taggit.managers import TaggableManager
# https://github.com/alex/django-taggit
# tags = TaggableManager()
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign, get_objects_for_user, get_perms

from whyqd.snippets.shrtn import surl, lurs

#########################################################################################################################################
# Main Wiqi Class
#########################################################################################################################################

class WiqiManager(models.Manager):
    """
    Generates a new QuerySet method and extends the original query object manager in the Model
    """
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    
class Wiqi(models.Model):
    """
    Fixed point for wiqistack with methods for editing, discussion and listing history.
    Access to the stack must come from the reverse relationship..
    """
    is_live_from = models.DateTimeField(blank=True, null=True, default=datetime.now,
                                        verbose_name="Publish from", help_text="Leave blank to publish immediately, otherwise select a future publication date.")
    is_live_to = models.DateTimeField(blank=True, null=True,
                                      verbose_name="Publish until", help_text="Leave blank for permanent publication, otherwise select a date to end publication.")
    is_protected = models.BooleanField(default=False,
                                     verbose_name="Protected", help_text="If selected, the wiqi will be public but require permissions to edit.")
    is_private = models.BooleanField(default=False,
                                     verbose_name="Private", help_text="If unselected, the wiqi will be public.")
    tags = TaggableManager(blank=True,
                           verbose_name="Tags", help_text="Metadata tags can be used to group similar wiqis.")
    is_active = models.BooleanField(default=True)
    is_searchable = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    stack_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_ base", null=True)
    stack_object_id = models.PositiveIntegerField(null=True)
    stack = generic.GenericForeignKey("stack_content_type", "stack_object_id")
    forked_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_forked", null=True)
    forked_object_id = models.PositiveIntegerField(null=True)
    forked = generic.GenericForeignKey("forked_content_type", "forked_object_id")
    forklist = models.ManyToManyField("self", blank=True)
    merged_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_ merged", null=True)
    merged_object_id = models.PositiveIntegerField(null=True)
    merged = generic.GenericForeignKey("merged_content_type", "merged_object_id")
    next_wiqi = models.ForeignKey("self", related_name="%(app_label)s_%(class)s_ next", null=True)
    previous_wiqi = models.ForeignKey("self", related_name="%(app_label)s_%(class)s_ previous", null=True)
    wiqi_objects = WiqiManager() # To extend QuerySet in derived classes
    objects = models.GeoManager()

    class QuerySet(QuerySet):
        def published(self):
            """
            Complete set of filters as to whether object is currently published.
            """
            now = pytz.UTC.localize(datetime.now())
            return self.filter(
                               Q(is_live_from__lte = now) &
                               Q(is_active = True) & 
                               (Q(is_live_to__gte = now) | 
                               Q(is_live_to = None)))
        def private(self):
            return self.filter(is_private = True)
        def public(self):
            return self.filter(is_private = False)

    class Meta:
        app_label = "wiqi"
        permissions = (
                       # "change" permission is reserved for public objects.
                       ("can_create", "Can create new documents."),
                       ("can_view", "Can view private object."),
                       ("can_view_stack", "Can view history of private object."),
                       ("can_edit", "Can edit private object and its history."),
                       ("can_publish", "Can change publication status of private object."),
                       ("can_protect", "Can change object protection."),      
                       ("can_change_privacy", "Can change object privacy."),                 
                       ("can_revert", "Can revert live object from historical object."),
                       ("can_fork", "Can fork the object to a new wiqi."),
                       ("can_merge", "Can merge the object into an existing wiqi."),
                       ("can_tag", "Can add tags."),
                       # Access to any of the above properties doesn't apply the right to share any of these with others. Unless below also included.
                       ("can_share_view", "Can share access of private object with others."),
                       ("can_share_view_stack", "Can share access of view history."),
                       ("can_share_edit", "Can share access of edit private object."),
                       ("can_share_publish", "Can share access of change publication status."),
                       ("can_share_protection", "Can share access of change object protection."),
                       ("can_share_privacy", "Can share access of change object privacy."),
                       ("can_share_revert", "Can share access of revert live object."),
                       ("can_share_fork", "Can share access of fork to a new wiqi."),
                       ("can_share_merge", "Can share access of merge into an existing wiqi."),
                       ("can_share_tag", "Can share access of add tags."),
                       )

    @models.permalink
    def get_absolute_url(self):
        # http://stackoverflow.com/a/4863504/295606
        return ('view_wiqi_full', (), {'wiqi_surl': self.merged_surl})
    @models.permalink
    def get_url(self):
        # For short url address
        return ('view_wiqi', (), {'wiqi_surl': self.merged_surl})
    @models.permalink
    def get_edit_url(self):
        return ('edit_wiqi', (), {'wiqi_type': self.get_class, 'wiqi_surl': self.stack.surl})
    @models.permalink
    def get_revert_url(self):
        return self.get_stacklist_url
    @models.permalink
    def get_fork_url(self):
        return ('fork_wiqi', (),{'wiqi_type': self.get_class, 'wiqi_surl': self.stack.surl})
    @models.permalink
    def get_merge_url(self):
        return ('merge_wiqi', (), {'wiqi_surl': self.surl})
    @models.permalink
    def get_stacklist_url(self):
        return ('view_wiqistacklist', (), {'wiqi_surl': self.surl})
    @models.permalink
    def get_share_url(self):
        return ('share_wiqi', (), {'wiqi_surl': self.surl})

    def __unicode__(self):
        return surl(self.id)

    @property
    def surl(self):
        return surl(self.id)

    @property
    def merged_surl(self):
        # Once merged it will always refer to the merged wiqi, although the stack is still accessable
        if self.merged:
            return self.merged.surl
        else:
            return self.surl

    @property
    def get_class(self):
        """
        Class name is commonly used and this saves typing
        """
        if self.stack:
            return self.stack.__class__.__name__.lower()
        else:
            return None
    
    def set_tags(self, **kwargs):
        if kwargs.get("tags",False):
            if self.id is None:
                self.save()
            else:
                self.tags.clear()
            self.tags.add(*kwargs["tags"])
            self.save()
        return self

    def set(self, **kwargs):
        self.is_live_from = kwargs.get("is_live_from", pytz.UTC.localize(datetime.now()))
        self.is_live_to = kwargs.get("is_live_to",None)
        self.is_private = kwargs.get("is_private",False)
        self.save()
        
    def update(self, **kwargs):
        """
        Only update if a first wiqi component exists in the stack, if not raise an error.
        """
        if self.id == None:
            raise
        if self.stack != None:
            # Has already got an assigned wiqistack
            new_base = self.stack.update(**kwargs)
            if new_base:
                self.stack = new_base
                self.save()
        else:
            # Is a new wiqi
            new_base = kwargs["WiqiStack"]()
            new_base.set(**kwargs)
            self.stack = new_base
            self.save()

    def discussion_update(self, **kwargs):
        try:
            assert(kwargs["discussion"] == self.discussion)
        except AssertionError, e:
            self.discussion = kwargs.get("discussion", None)
            self.save()

    @property
    def stacklist(self):
        """
        Return an ordered list of the stack history.
        """
        # http://stackoverflow.com/a/4863504/295606
        # http://stackoverflow.com/a/2064875/295606
        # self_type = ContentType.objects.get_for_model(self)
        # return self.stack.__class__.wiqi_objects.filter(wiqi_content_type__pk=self_type.id, wiqi_object_id=self.id).reverse()
        return self.stack.__class__.wiqi_objects.filter(wiqi=self.id).reverse()

    def fork(self, **kwargs):
        """
        Create a clone of the current wiqi and return it.
        """
        return self.stack.fork(**kwargs)
    
    def merge(self, merge_stack):
        self.merged = merge_stack
        self.save()

    @property
    def remove(self):
        self.is_active = False
        self.is_deleted = True
        self.save()
        
    def can_do(self, usr, permission):
        '''
        Return whether the user has rights for a specific permission for this wiqi.
        Anyone can view public wiqis, however.  Viewing the stack requires permissions.
        '''
        if permission == "can_view" and not self.is_private:
            return True
        if not self.is_private and not self.is_protected and usr.is_authenticated():
            return True
        if self.is_private and usr.has_perm(permission, self) and usr.profile.is_subscribed:
            return True
        if not self.is_private and usr.has_perm(permission, self):
            return True
        return False
        
    def assign_all_perm(self, usr):
        for perm, perm_text in self._meta.permissions:
            assign(perm, usr, self)

    # Shortcuts to stack
    @property
    def htmlresponse(self):
        return self.stack.htmlresponse
    @property
    def creator(self):
        return self.stack.creator
    @property
    def creator_ip(self):
        return self.stack.creator_ip
    @property
    def created_on(self):
        return self.stack.created_on
    @property
    def jsonresponse(self):
        return self.stack.jsonresponse
    @property
    def is_top_of_stack(self):
        return self.stack.is_top_of_stack
    
#########################################################################################################################################
# Abstract WiqiStack
#########################################################################################################################################

class WiqiStack(models.Model):
    """
    The base wiqi class containing the common elements and functions for all
    the required wiqis.
    """
    title = models.CharField(blank=True, max_length=250,
                            verbose_name="Title", help_text="This may be used as a title, section or figure heading.")
    description = models.TextField(blank=True,
                                   verbose_name="Description", help_text="May only be necessary where the content may not provide sufficient context.")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    creator_ip = models.GenericIPAddressField(blank=True, null=True, default="255.255.255.255")
    created_on = models.DateTimeField(auto_now_add=True)
    #original_creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    license = models.CharField(max_length=500, blank=True,
                               verbose_name="Release License", help_text="What form of copyright do you offer?")
    wiqi = models.ForeignKey(Wiqi, null=True)
    reverted_from_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_ reverted_from", null=True)
    reverted_from_object_id = models.PositiveIntegerField(null=True)
    reverted_from = generic.GenericForeignKey("reverted_from_content_type", "reverted_from_object_id")
    wiqi_objects = WiqiManager() # To extend QuerySet in derived classes
    objects = models.GeoManager()
    
    class QuerySet(QuerySet):
        def range(self, range_from=None, range_to=None):
            """
            Return a stack queryset according to a given date range.
            """
            if not range_from and not range_to:
                return self
            if not range_from:
                return self.filter(created_on__lte = range_to)
            if not range_to:
                return self.filter(created_on__gte = range_from)
            return self.filter(
                               Q(created_on__lte = range_to) &
                               Q(created_on__gte = range_from))
    
    class Meta:
        abstract = True
        app_label = "wiqi"
        get_latest_by = "created_on"
        ordering = ("created_on", )

    @models.permalink
    def get_absolute_url(self):
        # http://stackoverflow.com/a/4863504/295606
        return ('view_wiqistack', (), {'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    @models.permalink
    def get_url(self):
        # For short url address
        return ('view_wiqi', (), {'wiqi_surl': self.wiqi.merged_surl})
    @models.permalink
    def get_edit_url(self):
        return ('edit_wiqi', (),{'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    @models.permalink
    def get_revert_url(self):
        return ('revert_wiqi', (),{'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    @models.permalink
    def get_fork_url(self):
        return ('fork_wiqi', (),{'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    @models.permalink
    def get_stacklist_url(self):
        return ('view_wiqistacklist', (),{'wiqi_surl': self.wiqi_surl})
    @models.permalink
    def get_share_url(self):
        return ('share_wiqi', (),{'wiqi_surl': self.wiqi_surl})
    
    def __unicode__(self):
        return surl(self.id) #"Name: %s | Description: %s" % (self.title, self.description)

    @property
    def surl(self):
        """
        Surl is generated direct from primary key id.
        """
        return surl(self.id)
    
    @property
    def wiqi_surl(self):
        """
        Surl is generated direct from primary key id.
        """
        return surl(self.wiqi.id)
    
    @property
    def get_class(self):
        """
        Class name is commonly used and this saves typing
        """
        return self.__class__.__name__.lower()
    
    @property
    def is_top_of_stack(self):
        return self.id == self.wiqi.stack.id
    
    def set(self, **kwargs):
        self.title = kwargs.get("title", "")[:250]
        self.creator = kwargs["creator"]
        self.creator_ip =kwargs.get("creator_ip",None)
        #self.original_creator = kwargs["original_creator"]
        self.reverted_from = kwargs.get("reverted_from", None)
        self.license = kwargs.get("license","")
        self.wiqi = kwargs["wiqi"]
        self.save()

    def update(self, **kwargs):
        """
        Test whether there are any changes
        This does not explicitly raise an exception since the function will be inherited into a try-except
        """
        assert(kwargs["title"] == self.title)
        # assert(kwargs["many"].difference(self.many.all()) == set([]))

    def copy(self):
        """
        Provide a deep copy of itself for use in forks
        https://docs.djangoproject.com/en/1.5/topics/db/queries/
        If new related objects created (other than default), inherit this class.
        """
        copy_wiqi = self.wiqi
        copy_reverted_from = self.reverted_from
        self.pk = None
        self.id = None
        self.save()
        self.wiqi = copy_wiqi
        self.reverted_from = copy_reverted_from
        self.save()
        return self
        # Replace this entirely if you need additional related copies
        
    def fork(self, **kwargs):
        """
        Create a clone of the current wiqi and return it.
        """
        # http://stackoverflow.com/a/2064875/295606
        new_fork = Wiqi() # self.wiqi.__class__()
        # Ensure that this doesn't get reverted to None with future sets
        new_fork.forked = self
        new_fork.set(**kwargs)
        self.wiqi.forklist.add(new_fork)
        # Clone the wiqi
        new_fork.stack = self.copy()
        # Get the object rewired correctly pointing at new Wiqi
        new_fork.stack.wiqi = new_fork
        new_fork.save()
        self.wiqi = new_fork
        self.save()
        return new_fork

    def revert(self, ObjectStack, **kwargs):
        """
        Creates a new stack item copying all the content from the original but replacing with the user information of the revertor.
        """
        try:
            # Any attempt to revert to itself will fail
            assert(self.reverted_from == self)
        except AssertionError:
            # Only if it is different can we proceed
            kwargs["reverted_from"] = self
            kwargs["wiqi"] = self.wiqi
            kwargs["title"] = self.title
            new_base = ObjectStack()
            new_base.set(**kwargs)
            self.wiqi.stack = new_base
            self.wiqi.save()