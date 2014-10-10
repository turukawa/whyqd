from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Q
import hashlib
import pytz
from datetime import datetime, timedelta
from whyqd.novel.models import Novel
from jsonfield import JSONField
from decimal import Decimal

class TokenQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/dev/topics/db/managers/#calling-custom-queryset-methods-from-the-manager
    def issued_list(self, user):
        """
        Return filtered list of active and valid tokens.
        """
        deadline = pytz.UTC.localize(datetime.now()) - timedelta(days=settings.TOKEN_DELTA)
        return self.filter(Q(creator=user) &
                           (Q(is_valid=True) |
                           Q(redeemed_on__gt=deadline))
        )
    
    def valid_purchased(self, user, valid=True):
        """
        Return filtered list of valid purchased tokens.
        For use in potentially resending or changing, or requesting refund.
        Can set valid=False to get a list of purchased tokens already redeemed.
        """
        return self.filter(Q(creator=user) &
                           Q(is_valid=valid) &
                           Q(is_purchased=True)
        )

class TokenManager(models.Manager):
    def get_queryset(self):
        return TokenQuerySet(self.model, using=self._db)

    def issued_list(self, user):
        return self.get_queryset().issued_list(user)

class Token(models.Model):
    surl = models.CharField(max_length=32, blank=True, verbose_name="Short URL")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="%(class)s_creator")
    creator_ip = models.GenericIPAddressField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    redeemer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="%(class)s_redeemer")
    redeemer_ip = models.GenericIPAddressField(blank=True, null=True)
    redeemed_on = models.DateTimeField(blank=True, null=True)
    novel = models.ForeignKey(Novel, blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    is_purchased = models.BooleanField(default=False)
    #charge = JSONField(blank=True, null=True)
    #price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    recipient = models.EmailField(blank=True, null=True, verbose_name="Email")
    query = TokenManager()

    class Meta:
        app_label = "novel"
        verbose_name_plural = "Tokens"

    @models.permalink
    def get_token_redemption_url(self):
        return 'redeem_token', (), {'surl': self.surl}

    def issue(self, **kwargs):
        """
        Issue a token for sending.
        :param kwargs:
        :return:
        """
        self.creator = kwargs["creator"]
        self.creator_ip = kwargs.get("creator_ip", None)
        self.novel = kwargs["novel"]
        self.recipient = kwargs["recipient"]
        self.is_purchased = kwargs.get("is_purchased", False)
        #self.charge = kwargs.get("charge", None)
        #self.price = kwargs.get("price", Decimal("0.00"))
        # if purchased, and the creator and recipient are the same, then the person is buying this themselves
        # (i.e.) not a gift - and the book is being automatically sent...
        if not kwargs["creator"] or (kwargs.get("is_purchased", False) and kwargs["creator"].email == kwargs["recipient"]):
            self.is_valid = False
            self.redeemer = kwargs["creator"]
            self.redeemer_ip = kwargs.get("creator_ip", None)
            self.redeemed_on = pytz.UTC.localize(datetime.now())
        self.save()
        self.surl = hashlib.md5(''.join((settings.TOKEN_SALT, str(self.id)))).hexdigest()
        self.save()

    def edit(self, recipient):
        """
        Only return True if the token is still valid, otherwise leave it as is.
        :param recipient:
        :return:
        """
        if self.is_valid:
            self.recipient = recipient
            self.created_on = pytz.UTC.localize(datetime.now())
            self.save()
            return True
        else:
            return False

    def redeem(self, **kwargs):
        self.is_valid = False
        self.redeemer = kwargs["redeemer"]
        self.redeemer_ip = kwargs.get("redeemer_ip", None)
        self.redeemed_on = pytz.UTC.localize(datetime.now())
        self.save()
        if self.is_purchased:
            view_perm = "owns"
        else:
            view_perm = "borrowed"
        kwargs["redeemer"].take_ownership(self.novel, view_perm)

    def remove(self):
        """
        Automatically sets token as invalid.
        IMPORTANT: if this has been purchased then a refund must be managed elsewhere!
        :return:
        """
        self.is_valid = False
        self.redeemed_on = pytz.UTC.localize(datetime.now())
        self.save()
    
    @property
    def days_left(self):
        try:
            return (self.redeemed_on + timedelta(days=settings.TOKEN_DELTA) - pytz.UTC.localize(datetime.now())).days
        except:
            return False
    