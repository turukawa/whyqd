from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django_facebook.models import FacebookModel
from guardian.shortcuts import assign_perm, get_objects_for_user, remove_perm
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from whyqd.novel.models import Novel
from decimal import Decimal


class User(AbstractUser, FacebookModel):
    current_view = models.CharField(max_length=32, blank=True, verbose_name="Current chapter view.")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    @property
    def get_logout_url(self):
        return reverse('account_logout')
    
    def get_novel(self):
        novel_objects = get_objects_for_user(self, "owns", klass=Novel)
        if novel_objects:
            return novel_objects[0]
        return False

    def manage_novel(self):
        novel_object = self.get_novel()
        if novel_object:
            return reverse('issue_tokens', kwargs={'surl': novel_object.surl})
        return False
    
    def take_ownership(self, novel_object, view_perm):
        """
        Assign appropriate permissions to user for access after purchase or being loaned the novel.
        :param kwargs:
        :return:
        """
        for chapter in novel_object.chapterlist.all():
            assign_perm(view_perm, self, chapter)
        assign_perm(view_perm, self, novel_object)
    
    def current_token(self, purchased=False):
        return self.token_redeemer.filter(is_purchased=purchased).order_by('-redeemed_on')[0]

    def deadline(self, token_object=None):
        try:
            if not token_object:
                token_object = self.current_token()
            return token_object.redeemed_on + timedelta(days=settings.TOKEN_DELTA)
        except:
            return False
        
    def return_borrowed(self, novel_object, token_object):
        """
        Remove all borrowed permissions on the novel
        :param novel_object:
        :return:
        """
        if novel_object.get_class == "text":
            novel_object = novel_object.novel_chapterlist.all()[0]
        remove_perm("borrowed", self, novel_object)
        for chapter in novel_object.chapterlist.all():
            remove_perm("borrowed", self, chapter)
        token_object.delete()       

    def can_read(self, novel_object):
        """
        If novel is owned then True; if novel is borrowed, check if still valid and return status;
        If not valid, removed borrowed permissions;
        :param novel_object:
        :return:
        """
        if self.has_perm("owns", novel_object):
            return "owns"
        if self.has_perm("borrowed", novel_object):
            token_object = self.current_token()
            if self.deadline(token_object) and self.deadline(token_object) > pytz.UTC.localize(datetime.now()):
                return "borrowed"
            else:
                self.return_borrowed(novel_object, token_object)
        return False

    def can_read_terms(self, item):
        """
        Return the text version of the terms of readership for a particular item
        :param kwargs:
        :return:
        """
        if self.has_perm("owns", item):
            return "You own %s." % item.title
        if self.has_perm("borrowed", item):
            token_object = self.current_token()
            # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            deadline = self.deadline(token_object).strftime('%d %B %Y')
            return "%s has lent you %s until %s." % (token_object.creator.facebook_name, item.title, deadline)
        return "You don't have access to %s." % item.title

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
