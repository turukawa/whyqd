"""
Wiqi database schema
-------------------------------

Abstract classes:

        Wiqi:
                    is_live_from
                    is_live_to
                    is_active
                    is_private
                    is_searchable
                    is_deleted
                    stack (generic foreign key)
                    branched (generic foreign key)
                    branchlist
                    merged (generic foreign key)
                    next_wiqi
                    previous_wiqi
        WiqiStack:
                    title
                    description
                    creator
                    creator_ip
                    created_on
                    licence
                    citation
                    jsonresponse
                    reverted_from (generic foreign key)
                    wiqi (generic foreign key)

Derived classes:
        
        Components:
                Wiqi -> Component(WiqiStack)
"""

from django.db import models, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.query import QuerySet
from django.db.models import Q
# Allowing generic relations - https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/
#         content_type = models.ForeignKey(ContentType)
#         object_id = models.PositiveIntegerField()
#         content_object = generic.GenericForeignKey("content_type", "object_id")
from django.conf import settings
from django.core.urlresolvers import reverse

from datetime import datetime
from bs4 import BeautifulSoup
import pytz
from jsonfield import JSONField
import collections
import shortuuid as shrtn
from decimal import Decimal
# Google Diff Match Patch library
# http://code.google.com/p/google-diff-match-patch
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms

LICENSE_CHOICE = (("(c)","All Rights Reserved"),
                  ("CC0","No Rights Reserved"),
                  ("CC BY","CC Attribution"),
                  ("CC BY-ND","CC Attribution + NoDerivatives"),
                  ("CC BY-SA","CC Attribution + ShareAlike"),
                  ("CC BY-NC","CC Attribution + Noncommercial"),
                  ("CC BY-NC-ND","CC Attribution + Noncommercial + NoDerivatives"),
                  ("CC BY-NC-SA","CC Attribution + Noncommercial + ShareAlike"))

READ_IF_CHOICE = (("open","Open"),
                  ("login","Login"),
                  ("own","Own"))

CURRENCY_CHOICE = (("gbp","&pound;"),
    ("usd","$"),
    ("eur","&euro;"))

#########################################################################################################################################
# Main Wiqi Class
#########################################################################################################################################

class WiqiManager(models.Manager):
    """
    Generates a new QuerySet method and extends the original query object manager in the Model
    """
    def get_queryset(self):
        return self.model.QuerySet(self.model)
    
class Wiqi(models.Model):
    """
    Fixed point for wiqistack with methods for editing and listing history.
    Access to the stack must come from the reverse relationship..
    """
    surl = models.CharField(max_length=16, unique=True, verbose_name="Short URL")
    is_live_from = models.DateTimeField(blank=True, null=True, default=datetime.now, verbose_name="Publish from", 
                                        help_text="Leave blank to publish immediately, otherwise select a future publication date.")
    is_live_to = models.DateTimeField(blank=True, null=True, verbose_name="Publish until", 
                                      help_text="Leave blank for permanent publication, otherwise select a date to end publication.")
    is_private = models.BooleanField(default=False, verbose_name="Private", 
                                     help_text="If unselected, the wiqi will be public.")
    is_active = models.BooleanField(default=True)
    is_searchable = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    stack_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_base", null=True)
    stack_object_id = models.PositiveIntegerField(null=True)
    stack = generic.GenericForeignKey("stack_content_type", "stack_object_id")
    branched_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_branched", null=True)
    branched_object_id = models.PositiveIntegerField(null=True)
    branched = generic.GenericForeignKey("branched_content_type", "branched_object_id")
    branchlist = models.ManyToManyField("self", blank=True)
    merged_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_merged", null=True)
    merged_object_id = models.PositiveIntegerField(null=True)
    merged = generic.GenericForeignKey("merged_content_type", "merged_object_id")
    next_wiqi = models.ForeignKey("self", related_name="%(app_label)s_%(class)s_next", null=True)
    previous_wiqi = models.ForeignKey("self", related_name="%(app_label)s_%(class)s_previous", null=True)
    currency = models.CharField(max_length=7, choices=CURRENCY_CHOICE, default="gbp")
    read_if = models.CharField(max_length=5, choices=READ_IF_CHOICE, default="open")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    wiqi_objects = WiqiManager() # To extend QuerySet in derived classes

    class QuerySet(QuerySet):
        # https://docs.djangoproject.com/en/dev/topics/db/managers/#calling-custom-queryset-methods-from-the-manager
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
                       ("can_change_privacy", "Can change object privacy."),                 
                       ("can_revert", "Can revert live object from historical object."),
                       ("can_branch", "Can branch the object to a new wiqi."),
                       ("can_merge", "Can merge the object into an existing wiqi."),
                       ("owns", "Has purchased the object."),
                       ("borrowed", "Has borrowed the object."),
                       # Access to any of the above properties doesn't apply the right to share any of these with others. Unless below also included.
                       ("can_share_view", "Can share access of private object with others."),
                       ("can_share_view_stack", "Can share access of view history."),
                       ("can_share_edit", "Can share access of edit private object."),
                       ("can_share_publish", "Can share access of change publication status."),
                       ("can_share_privacy", "Can share access of change object privacy."),
                       ("can_share_revert", "Can share access of revert live object."),
                       ("can_share_branch", "Can share access of branch to a new wiqi."),
                       ("can_share_merge", "Can share access of merge into an existing wiqi."),
                       )

    def get_absolute_url(self):
        # http://stackoverflow.com/a/4863504/295606
        return reverse('view_wiqi_full', kwargs={'wiqi_surl': self.merged_surl})
    def get_url(self):
        # For short url address
        return reverse('view_wiqi', kwargs={'wiqi_surl': self.merged_surl})
    def get_edit_url(self):
        return reverse('edit_wiqi', kwargs={'wiqi_type': self.get_class, 'wiqi_surl': self.stack.surl})
    def get_revert_url(self):
        return self.get_stacklist_url
    def get_branch_url(self):
        return reverse('branch_wiqi', kwargs={'wiqi_type': self.get_class, 'wiqi_surl': self.stack.surl})
    def get_merge_url(self):
        return reverse('merge_wiqi', kwargs={'wiqi_surl': self.surl})
    def get_stacklist_url(self):
        return reverse('view_wiqistacklist', kwargs={'wiqi_surl': self.surl})
    def get_share_url(self):
        return reverse('share_wiqi', kwargs={'wiqi_surl': self.surl})

    def __unicode__(self):
        return self.surl

    @property
    def merged_surl(self):
        # Once merged it will always refer to the merged wiqi, although the stack is still accessable
        if self.merged:
            return self.merged.surl
        else:
            return self.surl
        
    @property
    def base_wiqi(self):
        """
        Return the Wiqi where such ambiguity causes problems.
        """
        return self

    @property
    def get_class(self):
        """
        Class name is commonly used and this saves typing
        """
        if self.stack:
            return self.stack.__class__.__name__.lower()
        else:
            return None
    
    @property
    def get_next(self):
        if self.next_wiqi:
            return self.next_wiqi.surl
        else:
            return ""
    @property
    def get_previous(self):
        if self.previous_wiqi:
            return self.previous_wiqi.surl
        else:
            return ""

    def set(self, **kwargs):
        shrtn.set_alphabet(settings.SURL_ALPHABET)
        while True:
            # the surl must be unique and the likelihood of clash is low, so try again
            try:
                self.surl = shrtn.ShortUUID().random(length=settings.SURL_LENGTH)
                self.save()
            except IntegrityError:
                continue
            else:
                break
        self.is_live_from = kwargs.get("is_live_from", pytz.UTC.localize(datetime.now()))
        self.is_live_to = kwargs.get("is_live_to",None)
        self.is_private = kwargs.get("is_private",False)
        self.next_wiqi = kwargs.get("next", None)
        self.previous_wiqi = kwargs.get("previous", None)
        self.save()
        
    def update(self, **kwargs):
        """
        Only update if a first wiqi component exists in the stack, if not raise an error.
        """
        if self.id == None:
            raise
        kwargs["wiqi"] = self
        if self.stack != None:
            # Has already got an assigned wiqistack
            new_base = self.stack.update(**kwargs)
        else:
            # Is a new wiqi
            new_base = kwargs["WiqiStack"]()
            new_base.set(**kwargs)
        if new_base:
            self.stack = new_base
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

    def branch(self, **kwargs):
        """
        Create a branch of the current wiqi and top wiqistack and return
        the new wiqi.
        """
        return self.stack.branch(**kwargs)
    
    def merge(self, merge_stack):
        self.merged = merge_stack
        self.save()

    @property
    def remove(self):
        self.is_active = False
        self.is_deleted = True
        self.save()
        return self
        
    def can_do(self, usr, permission):
        '''
        Return whether the user has rights for a specific permission for this wiqi.
        Anyone can view public wiqis, however.  Viewing the stack requires permissions.
        '''
        if permission == "can_view" and not self.is_private:
            return True
        if not self.is_private and usr.is_authenticated():
            return True
        if self.is_private and usr.has_perm(permission, self) and usr.profile.is_subscribed:
            return True
        if not self.is_private and usr.has_perm(permission, self):
            return True
        return False
        
    def assign_all_perm(self, usr):
        for perm, perm_text in self._meta.permissions:
            assign_perm(perm, usr, self)

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
    surl = models.CharField(max_length=16, unique=True, verbose_name="Short URL")
    title = models.CharField(blank=True, max_length=250, verbose_name="Title", 
                             help_text="This may be used as a title, section or figure heading.")
    description = models.TextField(blank=True, verbose_name="Description", 
                                   help_text="May only be necessary where the content may not provide sufficient context.")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="%(app_label)s_%(class)s_creator")
    creator_ip = models.GenericIPAddressField(blank=True, null=True, default="255.255.255.255")
    created_on = models.DateTimeField(auto_now_add=True)
    license = models.CharField(max_length=50, choices=LICENSE_CHOICE, default="All Rights Reserved", 
                               verbose_name="Release License", help_text="What form of copyright do you offer?")
    citation = models.CharField(max_length=150, blank=True, default="",
                                help_text="Please reference the original creator, if it wasn't you.")
    jsonresponse = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, blank=True, null=True)
    #original_creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    wiqi = models.ForeignKey(Wiqi, null=True)
    reverted_from_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_reverted_from",
                                                   null=True, blank=True)
    reverted_from_object_id = models.PositiveIntegerField(null=True, blank=True)
    reverted_from = generic.GenericForeignKey("reverted_from_content_type", "reverted_from_object_id")
    wiqi_objects = WiqiManager() # To extend QuerySet in derived classes
    
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

    def get_absolute_url(self):
        # http://stackoverflow.com/a/4863504/295606
        return reverse('view_wiqistack', kwargs={'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    def get_url(self):
        # For short url address
        return reverse('view_wiqi', kwargs={'wiqi_surl': self.wiqi.merged_surl})
    def get_edit_url(self):
        return reverse('edit_wiqi', kwargs={'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    def get_revert_url(self):
        return reverse('revert_wiqi', kwargs={'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    def get_branch_url(self):
        return reverse('branch_wiqi', kwargs={'wiqi_type': self.get_class, 'wiqi_surl': self.surl})
    def get_stacklist_url(self):
        return reverse('view_wiqistacklist', kwargs={'wiqi_surl': self.wiqi_surl})
    def get_share_url(self):
        return reverse('share_wiqi', kwargs={'wiqi_surl': self.wiqi_surl})

    def __unicode__(self):
        return self.surl #"Name: %s | Description: %s" % (self.title, self.description)

    @property
    def wiqi_surl(self):
        """
        Surl is generated direct from primary key id.
        """
        return self.wiqi.surl
    
    @property
    def get_class(self):
        """
        Class name is commonly used and this saves typing
        """
        return self.__class__.__name__.lower()
    
    @property
    def is_top_of_stack(self):
        return self.id == self.wiqi.stack.id
    
    @property
    def base_wiqi(self):
        """
        Return the Wiqi from the WiqiStack where such ambiguity causes problems.
        """
        return self.wiqi
    
    def set(self, **kwargs):
        shrtn.set_alphabet(settings.SURL_ALPHABET)
        while True:
            # the surl must be unique and the likelihood of clash is low, so try again
            try:
                self.surl = shrtn.ShortUUID().random(length=settings.SURL_LENGTH)
                self.save()
            except IntegrityError:
                continue
            else:
                break
        self.title = kwargs["title"]
        self.creator = kwargs["creator"]
        self.creator_ip =kwargs.get("creator_ip",None)
        self.license = kwargs.get("license","All Rights Reserved")
        self.citation = kwargs.get("citation", "")
        #self.original_creator = kwargs["original_creator"]
        self.reverted_from = kwargs.get("reverted_from", None)
        self.wiqi = kwargs["wiqi"]
        self.save()

    def update(self, **kwargs):
        """
        Test whether there are any changes
        This does not explicitly raise an exception since the function will be inherited into a try-except
        """
        assert(kwargs["title"] == self.title)
        # assert(kwargs["many"].difference(self.many.all()) == set([]))

    def preprocess(self, **kwargs):
        kwargs["title"] = BeautifulSoup(kwargs.get("title", "")[:250]).get_text().strip()
        return kwargs

    def copy(self, **kwargs):
        """
        Provide a deep copy of itself for use in branches
        https://docs.djangoproject.com/en/1.7/topics/db/queries/#copying-model-instances
        If new related objects created (other than default), inherit this class.
        !!!! This is going to need review based on the unique surl attributes. !!!!!
        !!!! This is NOT tested. !!!!!
        """
        shrtn.set_alphabet(settings.SURL_ALPHABET)
        while True:
            # the surl must be unique and the likelihood of clash is low, so try again
            try:
                self.surl = shrtn.ShortUUID().random(length=settings.SURL_LENGTH)
                self.pk = None
                self.id = None
                self.save()
            except IntegrityError:
                continue
            else:
                break
        self.creator = kwargs.get("creator", self.creator)
        self.creator_ip = kwargs.get("creator_ip", self.creator_ip)
        self.save()
        return self
        # Replace this entirely if you need additional related copies
        
    def branch(self, **kwargs):
        """
        Create a clone of the current wiqi and return it.
        """
        # http://stackoverflow.com/a/2064875/295606
        new_branch = Wiqi() # self.wiqi.__class__()
        # Ensure that this doesn't get reverted to None with future sets
        new_branch.branched = self
        new_branch.set(**kwargs)
        self.wiqi.branchlist.add(new_branch)
        # Clone the wiqi
        new_branch.stack = self.copy(**kwargs)
        # Get the object rewired correctly pointing at new Wiqi
        new_branch.stack.wiqi = new_branch
        new_branch.save()
        self.wiqi = new_branch
        self.save()
        return self.wiqi

    def revert(self, ObjectStack, **kwargs):
        """
        Creates a new stack item copying all the content from the original but replacing with the user information of 
        the revertor.
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