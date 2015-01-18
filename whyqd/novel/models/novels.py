from django.db import models, IntegrityError
from django.core.urlresolvers import reverse
from whyqd.wiqi.models import Wiqi

from django.conf import settings
from guardian.shortcuts import assign_perm

from bs4 import BeautifulSoup
from jsonfield import JSONField
import collections
import shortuuid as shrtn
import re

LICENSE_CHOICE = (("(c)","All Rights Reserved"),
                  ("CC0","No Rights Reserved"),
                  ("CC BY","CC Attribution"),
                  ("CC BY-ND","CC Attribution + NoDerivatives"),
                  ("CC BY-SA","CC Attribution + ShareAlike"),
                  ("CC BY-NC","CC Attribution + Noncommercial"),
                  ("CC BY-NC-ND","CC Attribution + Noncommercial + NoDerivatives"),
                  ("CC BY-NC-SA","CC Attribution + Noncommercial + ShareAlike"))

#http://stackoverflow.com/a/1190866
def get_covername(self, filename):
    return '/'.join([self.creator.username, 'covers', filename])
def get_ebookname(self, filename):
    return '/'.join([self.creator.username, 'ebooks', filename])

class Novel(models.Model):
    """
    Fixed point for wiqistack with methods for editing and listing history.
    Access to the stack must come from the reverse relationship..
    """
    surl = models.CharField(max_length=16, unique=True, verbose_name="Short URL")
    title = models.CharField(blank=True, max_length=250, verbose_name="Title",
                             help_text="This may be used as a title, section or figure heading.")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="%(class)s_creator")
    creator_ip = models.GenericIPAddressField(blank=True, null=True, default="255.255.255.255")
    created_on = models.DateTimeField(auto_now_add=True)
    licensing = models.CharField(max_length=50, choices=LICENSE_CHOICE, default="(c)",
                               verbose_name="Release License", help_text="What form of copyright do you offer?")
    jsonresponse = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, blank=True, null=True)
    authors = models.CharField(max_length=250, blank=True,
                               verbose_name="Author names",
                               help_text="Comma-separated list of all authors.")
    authorsort = models.CharField(max_length=250, blank=True,
                                  verbose_name="Sortable author list",
                                  help_text="Author list by 'surname, name'; for listing.")
    pitch = models.CharField(max_length=503, blank=True,
                               verbose_name="Elevator Pitch",
                               help_text="You have 503 characters. Sell it to me.")
    summary = models.TextField(blank=True, verbose_name="Summary",
                               help_text="The back cover of your book.")
    language = models.CharField(max_length=50, blank=True,
                                verbose_name="Published language",
                                help_text="The language you're writing in.")
    series = models.CharField(max_length=150, blank=True,
                              verbose_name="Book series",
                              help_text="Is the book part of a series?")
    series_index = models.CharField(max_length=10, blank=True,
                                    verbose_name="Series index",
                                    help_text="What number in the series?")
    ISBN = models.CharField(max_length=40, blank=True,
                            verbose_name="13-digit ISBN for your book.",
                            help_text="Enter the 13-digit ISBN for your book. Can include dashes or spaces.")
    cover_image = models.ImageField(upload_to=get_covername, blank=True)
    chapterlist = models.ManyToManyField(Wiqi, related_name="%(class)s_chapterlist", blank=True, null=True)
    sentinal = models.OneToOneField(Wiqi, related_name="%(class)s_sentinal", blank=True, null=True)
    word_count = models.IntegerField(blank=True, null=True)
    cover_banner = models.ImageField(upload_to=get_covername, blank=True)
    cover_thumbnail = models.ImageField(upload_to=get_covername, blank=True)
    ebook_epub = models.FileField(upload_to=get_ebookname, blank=True)
    ebook_mobi = models.FileField(upload_to=get_ebookname, blank=True)
    ebook_pdf = models.FileField(upload_to=get_ebookname, blank=True)
    ebook_azw = models.FileField(upload_to=get_ebookname, blank=True)

    class Meta:
        # http://www.nomadjourney.com/2009/11/splitting-up-django-models/
        app_label = "novel"
        verbose_name_plural = "Novels"
        permissions = (
                       ("can_create", "Can create new novels."),
                       ("can_view", "Can view private novel."),
                       ("can_edit", "Can edit novel."),
                       ("can_publish", "Can change publication status of novel."),
                       ("can_share", "Can share access of novel with others."),
                       ("owns", "Has purchased the object."),
                       ("borrowed", "Has borrowed the object."),
                       )

    def get_absolute_url(self):
        # http://stackoverflow.com/a/4863504/295606
        return reverse('view_novel', kwargs={'surl': self.surl})

    def get_prices_url(self):
        return reverse('price_novel', kwargs={'surl': self.surl})

    def get_manage_tokens_url(self):
        return reverse('issue_tokens', kwargs={'surl': self.surl})

    def __unicode__(self):
        return self.surl #"Name: %s | Description: %s" % (self.title, self.description)

    @property
    def get_class(self):
        """
        Class name is commonly used and this saves typing
        """
        return self.__class__.__name__.lower()

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
        self.title = BeautifulSoup(kwargs.get("title", "")[:250]).get_text().strip()
        self.creator = kwargs["creator"]
        self.creator_ip = kwargs.get("creator_ip",None)
        self.licensing = kwargs.get("licensing","(c)")
        self.save()

    def assign_all_perm(self, usr):
        for perm, perm_text in self._meta.permissions:
            assign_perm(perm, usr, self)

    def refresh_chapters(self, wiqi_object):
        '''
        Process or Refresh all chapters to create the appropriate JSON file;
        :param wiqi_object:
        :return:
        '''
        self.word_count = 0
        self.sentinal = wiqi_object
        # Set the sentinal based on the first wiqi_object
        self.jsonresponse = {'words': self.word_count,
                             'chapters': {},
                             'order': {},
                             'sentinal': {'first': wiqi_object.surl,
                                          'last': wiqi_object.surl
                             }
        }
        count = 1
        while wiqi_object:
            self.word_count += wiqi_object.stack.word_count
            self.jsonresponse['words'] = self.word_count
            self.jsonresponse['chapters'][count] = {'title': wiqi_object.stack.title,
                                                    'subtitle': wiqi_object.stack.subtitle,
                                                    'url': wiqi_object.get_absolute_url(),
                                                    'surl': wiqi_object.surl,
                                                    #'price': wiqi_object.price,
                                                    #'read_if': wiqi_object.read_if,
                                                    }
            if wiqi_object.next_wiqi:
                next_wiqi = wiqi_object.next_wiqi.surl
            else:
                next_wiqi = None
            if wiqi_object.previous_wiqi:
                previous_wiqi = wiqi_object.previous_wiqi.surl
            else:
                previous_wiqi = None
            self.jsonresponse['order'][wiqi_object.surl] = {'next': next_wiqi,
                                                            'previous': previous_wiqi,
                                                            'i': count,
                                                            }
            self.jsonresponse['sentinal']['last'] = wiqi_object.surl
            wiqi_object = wiqi_object.next_wiqi
            count += 1
        self.save()
        return self

    def add_chapters(self, **kwargs):
        """
        Bulk upload function for receiving new chapters in the form:
            {i: {title: ... , content: ...} ...
        Create new Text chapters and then add them to this book
        """
        if kwargs.get("upload", False):
            self.chapterlist.clear()
            first_wiqi_object = None
            previous_wiqi_object = None
            for i in range(len(kwargs["upload"])):
                if kwargs["upload"][str(i)]: # in case blanks turn up
                    wiqi_object = Wiqi()
                    wiqi_kwargs = kwargs["upload"][str(i)]
                    wiqi_kwargs.update(kwargs["common"])
                    wiqi_object.set(**wiqi_kwargs)
                    wiqi_object.update(**wiqi_kwargs)
                    wiqi_object.assign_all_perm(kwargs["common"]["creator"])
                    if not first_wiqi_object:
                        first_wiqi_object = wiqi_object
                    if previous_wiqi_object:
                        # Assign the previous wiqi to this wiqi
                        wiqi_object.previous_wiqi = previous_wiqi_object
                        wiqi_object.save()
                        previous_wiqi_object.next_wiqi = wiqi_object
                        previous_wiqi_object.save()
                    previous_wiqi_object = wiqi_object
                    # Update the wiqi and novel chapterlist
                    self.chapterlist.add(wiqi_object)
                    wiqi_object.stack.jsonresponse['novelurl'] = self.surl
                    wiqi_object.stack.jsonresponse['noveltitle'] = self.title
                    wiqi_object.stack.save()
            return self.refresh_chapters(first_wiqi_object)
        return self

    @property
    def is_valid_isbn13(self):
        # http://stackoverflow.com/a/1249424
        isbn = re.sub("[^0-9]", "", self.ISBN)
        # http://en.wikipedia.org/wiki/International_Standard_Book_Number
        check = (10 - (sum(int(digit) * (3 if idx % 2 else 1) for idx, digit in enumerate(isbn[:12])) % 10)) % 10
        return check == int(isbn[-1])