from django.db import models, IntegrityError
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.urlresolvers import reverse
import shortuuid as shrtn
import pytz
from datetime import datetime, timedelta
from whyqd.novel.models import Novel
from jsonfield import JSONField
from decimal import Decimal

#http://character-code.com/currency-html-codes.php
CURRENCY_CHOICE = (("gbp","&pound;"),
    ("usd","$"),
    ("eur","&euro;"))

class TokenQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/dev/topics/db/managers/#calling-custom-queryset-methods-from-the-manager
    def issued_list(self, user):
        """
        Return filtered list of active and valid tokens.
        """
        deadline = pytz.UTC.localize(datetime.now()) - timedelta(days=settings.TOKEN_DELTA)
        return self.filter(Q(creator=user) &
                           Q(is_purchased=False) &
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
    def valid_purchased(self, user, valid=True):
        return self.get_queryset().valid_purchased(user, valid)

class Token(models.Model):
    surl = models.CharField(max_length=25, unique=True, verbose_name="Short URL")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="%(class)s_creator")
    creator_ip = models.GenericIPAddressField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    redeemer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="%(class)s_redeemer")
    redeemer_ip = models.GenericIPAddressField(blank=True, null=True)
    redeemed_on = models.DateTimeField(blank=True, null=True)
    stripe_id = models.CharField(max_length=30, verbose_name="Stripe ID", null=True, blank=True)
    novel = models.ForeignKey(Novel, blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    is_purchased = models.BooleanField(default=False)
    charge = JSONField(blank=True, null=True)
    currency = models.CharField(max_length=7, choices=CURRENCY_CHOICE, default="gbp")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    recipient = models.EmailField(blank=True, null=True, verbose_name="Email")
    query = TokenManager()

    class Meta:
        app_label = "novel"
        verbose_name_plural = "Tokens"

    def get_token_redemption_url(self):
        return reverse('redeem_token', kwargs={'surl': self.surl})

    def issue(self, **kwargs):
        """
        Issue a token for sending.
        :param kwargs:
        :return:
        """
        shrtn.set_alphabet(settings.SURL_ALPHABET)
        while True:
            # the surl must be unique and the likelihood of clash is low, so try again
            try:
                self.surl = shrtn.ShortUUID().random(length=settings.TOKEN_SURL_LENGTH)
                self.save()
            except IntegrityError:
                continue
            else:
                break
        self.creator = kwargs["creator"]
        self.creator_ip = kwargs.get("creator_ip", None)
        self.novel = kwargs["novel"]
        self.recipient = kwargs["recipient"]
        self.is_purchased = kwargs.get("is_purchased", False)
        self.charge = kwargs.get("charge", None)
        self.price = kwargs.get("price", Decimal("0.00"))
        self.currency = kwargs.get("currency", "gbp")
        self.stripe_id = kwargs.get("stripe_id", None)
        # if purchased, and the creator and recipient are the same, then the person is buying this themselves
        # (i.e.) not a gift, the person is logged in and they will automatically take ownership...
        if kwargs["creator"] and kwargs.get("is_purchased", False) and kwargs["creator"].email == kwargs["recipient"]:
            self.is_valid = False
            self.redeemer = kwargs["creator"]
            self.redeemer_ip = kwargs.get("creator_ip", None)
            self.redeemed_on = pytz.UTC.localize(datetime.now())
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
        self.redeemer = kwargs.get("redeemer", None)
        self.redeemer_ip = kwargs.get("redeemer_ip", None)
        self.redeemed_on = pytz.UTC.localize(datetime.now())
        self.save()
        if self.redeemer:
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
        self.is_purchased = False
        self.redeemed_on = pytz.UTC.localize(datetime.now())
        self.save()
    
    @property
    def days_left(self):
        try:
            return (self.redeemed_on.date()
                    + timedelta(days=settings.TOKEN_DELTA)
                    - pytz.UTC.localize(datetime.now()).date()).days
        except:
            return False
    