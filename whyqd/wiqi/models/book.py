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
                    reverted_from (generic foreign key)
                    wiqi (generic foreign key)

Derived classes:
        
        Components:
                Wiqi -> Component(WiqiStack)
"""
from base import *
import re

#########################################################################################################################################
# Derived Classes 
#########################################################################################################################################

#http://stackoverflow.com/a/1190866
def get_covername(self, filename):
    return '/'.join([self.creator.username, 'covers', filename])
def get_ebookname(self, filename):
    return '/'.join([self.creator.username, 'ebooks', filename])

class Book(WiqiStack):
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
    chapterlist = models.ManyToManyField(Wiqi, related_name="%(app_label)s_%(class)s_chapterlist", blank=True)
    # The below will be generated or processed...
    word_count = models.IntegerField(blank=True, null=True)
    cover_banner = models.ImageField(upload_to=get_covername, blank=True)
    cover_thumbnail = models.ImageField(upload_to=get_covername, blank=True)
    ebook_epub = models.FileField(upload_to=get_ebookname, blank=True)
    ebook_mobi = models.FileField(upload_to=get_ebookname, blank=True)
    
    class Meta(WiqiStack.Meta):
        db_table = "book"
        verbose_name_plural = "Books"
    
    def set(self, **kwargs):
        if not kwargs.get("set", False):
            kwargs = self.preprocess(**kwargs)
        self.authors = kwargs.get("authors", "")
        self.authorsort = kwargs.get("authorsort", "")
        self.pitch = kwargs.get("pitch", "")
        self.summary = kwargs.get("summary", "")
        self.language = kwargs.get("language", "")
        self.series = kwargs.get("series", "")
        self.series_index = kwargs.get("series_index", "")
        self.ISBN = kwargs.get("ISBN", "")
        self.cover_image = kwargs.get("cover_image", None)
        super(Book, self).set(**kwargs)
        self.postprocess(**kwargs)
    
    def update(self, **kwargs):
        if not kwargs.get("set", False):
            kwargs = self.preprocess(**kwargs)
        try:
            assert(self.authors == kwargs.get("authors", ""))
            assert(self.authorsort == kwargs.get("authorsort", ""))
            assert(self.pitch == kwargs.get("pitch", ""))
            assert(self.summary == kwargs.get("summary", ""))
            assert(self.language == kwargs.get("language", ""))
            assert(self.series == kwargs.get("series", ""))
            assert(self.series_index == kwargs.get("series_index", ""))
            assert(self.ISBN == kwargs.get("ISBN", ""))
            if kwargs.get("cover_image", False):
                assert(self.cover_image == kwargs["cover_image"])
            # http://stackoverflow.com/a/8866661
            assert(set(list(self.chapterlist.all())) == kwargs.get("chapterlist", []))
            super(Book, self).update(**kwargs)
            return False
        except AssertionError:
            new_base = self.copy(**kwargs)
            new_base.set(**kwargs)
            return new_base
    
    def update_link(self, wiqi_object):
        """
        Check if the wiqi_object is in the chapterlist and if its order has
        changed.
        """
        update_chapter = False
        if wiqi_object not in self.chapterlist.all():
            self.chapterlist.add(wiqi_object)
            wiqi_object.stack.jsonresponse['bookurl'] = self.wiqi_surl
            wiqi_object.stack.jsonresponse['booktitle'] = self.title
            wiqi_object.stack.save()
            update_chapter = True
        else:
            if wiqi_object.get_previous != self.jsonresponse['order'][wiqi_object.surl]['previous']:
                update_chapter = True
        if update_chapter:
            kwargs = {'linked_wiqi': wiqi_object}
            self = self.copy(**kwargs)
            self.wiqi.stack = self
            self.wiqi.save()
            self.postprocess(**kwargs)
        
    def reprocess(self):
        """
        Specific to the Book wiqi
        Every now and then (perhaps user-initiated) the chapters must be 
        reindexed and updated to ensure that the order of the chapters is 
        appropriately reflected.
        """
        chapters = dict.copy(self.jsonresponse['chapters'])
        self.jsonresponse['chapters'] = {}
        first_chapter = self.jsonresponse['sentinal']['next']
        next_chapter = first_chapter
        for i in range(1, len(self.jsonresponse['order'])+1):
            old_i = self.jsonresponse['order'][next_chapter]['i']
            self.jsonresponse['chapters'][str(i)] = dict.copy(chapters[old_i])
            self.jsonresponse['order'][next_chapter]['i'] = str(i)
            next_chapter = self.jsonresponse['order'][next_chapter]['next']
        self.save()
                        
    def preprocess(self, **kwargs):
        kwargs = super(Book, self).preprocess(**kwargs)
        kwargs["pitch"] = BeautifulSoup(kwargs.get("pitch","")[:503]).get_text().strip()
        kwargs["authorsort"] = BeautifulSoup(kwargs.get("authorsort","")[:250]).get_text().strip()
        kwargs["authors"] = BeautifulSoup(kwargs.get("authors","")[:250]).get_text().strip()
        kwargs["summary"] = BeautifulSoup(kwargs.get("summary","")).get_text().strip()
        kwargs["language"] = BeautifulSoup(kwargs.get("language","")[:50]).get_text().strip()
        kwargs["series"] = BeautifulSoup(kwargs.get("series","")[:150]).get_text().strip()
        kwargs["series_index"] = BeautifulSoup(kwargs.get("series_index","")[:10]).get_text().strip()
        kwargs["ISBN"] = BeautifulSoup(kwargs.get("ISBN","")[:40]).get_text().strip()
        kwargs["set"] = True
        return kwargs

    def postprocess(self, **kwargs):
        # Fix this later, but need to produce other cover images
        if not self.cover_image:
            self.cover_banner = None
            self.cover_thumbnail = None
            cover_url = None
        # Process the underlying chapters after the save...
        this = kwargs.get('linked_wiqi', False)
        if self.jsonresponse and this:
            if not self.jsonresponse.get('chapters', False):
                self.word_count = this.stack.word_count
                self.jsonresponse.update({'words': self.word_count,
                                         'chapters': {'1': {'title': this.stack.title,
                                                            'subtitle': this.stack.subtitle,
                                                            'url': this.get_absolute_url(),
                                                            #'price': this.price,
                                                            }
                                                      },
                                         'order': {this.surl: {'i': '1',
                                                               'next': this.surl,
                                                               'previous': this.surl,
                                                               }
                                                   },
                                         'sentinal': {'next': this.surl,
                                                      'previous': this.surl
                                                     }
                                         })
            else:
                count = len(self.jsonresponse['order']) + 1 #adding new chapter
                if this.previous_wiqi:
                    previous = this.previous_wiqi.surl
                    if not this.next_wiqi:
                        # This is the new last chapter
                        self.jsonresponse['sentinal']['previous'] = this.surl
                    old_next = self.jsonresponse['order'][previous]['next']
                    self.jsonresponse['order'][previous]['next'] = this.surl
                    self.jsonresponse['order'][old_next]['previous'] = this.surl
                    self.jsonresponse['order'][this.surl] = {'next': old_next,
                                                             'previous': previous,
                                                             'i': count,
                                                             }
                else:
                    # This is the new first chapter...
                    old_first = self.jsonresponse['sentinal']['next']
                    last = self.jsonresponse['sentinal']['previous']
                    self.jsonresponse['sentinal']['next'] = this.surl
                    self.jsonresponse['order'][last]['next'] = this.surl
                    self.jsonresponse['order'][old_first]['previous'] = this.surl
                    self.jsonresponse['order'][this.surl] = {'next': old_first,
                                                             'previous': last,
                                                             'i': count,
                                                             }
                self.jsonresponse['chapters'][count] = {'title': this.stack.title,
                                                        'subtitle': this.stack.subtitle,
                                                        'url': this.stack.get_absolute_url(),
                                                        #'price': chapter.price,
                                                        }            
                self.save()
                self.reprocess()
        else:
            self.jsonresponse = {'url': self.get_absolute_url(),
                                 'surl': kwargs['wiqi'].surl,
                                 'wiqiurl': self.get_url(),
                                 'cover': cover_url,
                                 'pitch': self.pitch,
                                 'summary': self.summary,
                                 'language': self.language,
                                 'author': self.authors,
                                 'title': self.title,
                                 'words': 0,
                                 'ISBN': self.ISBN,
                                 }
        self.save()

    def copy(self, **kwargs):
        """
        Provide a deep copy of itself for use in branches
        https://docs.djangoproject.com/en/1.5/topics/db/queries/
        If new related objects created (other than default), rewrite this class.
        """
        copy_chapterlist = self.chapterlist.all()
        self = super(Book, self).copy(**kwargs)
        # http://stackoverflow.com/a/10080118
        self.chapterlist.add(*copy_chapterlist)
        return self
        
    def revert(self, **kwargs):
        """
        Creates a new stack item copying all the content from the original but replacing with the user information of the revertor.
        """
        kwargs["authors"] = self.authors
        kwargs["authorsort"] = self.authorsort
        kwargs["pitch"] = self.pitch
        kwargs["summary"] = self.summary
        kwargs["language"] = self.language
        kwargs["series"] = self.series
        kwargs["series_index"] = self.series_index
        kwargs["ISBN"] = self.ISBN
        kwargs["cover_image"] = self.cover_image
        super(Book, self).revert(Book, **kwargs)

    @property
    def htmlresponse(self):
        # Any ideas as to what this should return?
        return self.content
    
    @property
    def is_valid_isbn13(self):
        # http://stackoverflow.com/a/1249424
        isbn = re.sub("[^0-9]", "", self.ISBN)
        # http://en.wikipedia.org/wiki/International_Standard_Book_Number
        check = (10 - (sum(int(digit) * (3 if idx % 2 else 1) for idx, digit in enumerate(isbn[:12])) % 10)) % 10
        return check == int(isbn[-1])