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
from base import *
# http://stackoverflow.com/a/1040027 and 
# http://stackoverflow.com/questions/5691129/save-image-from-url-in-django-and-checking-if-its-an-image
import imghdr
from whyqd.snippets import dominantcolor 

#########################################################################################################################################
# Derived Classes 
#########################################################################################################################################

#http://stackoverflow.com/a/1190866
def get_filename(self, filename):
    return '/'.join([self.creator.username, 'images', filename])

class Image(WiqiStack):
    file = models.ImageField(upload_to=get_filename)
    caption = models.CharField(max_length=200, blank=True,
                               verbose_name="Caption", 
                               help_text="A caption for the image.")
    source_attribution = models.CharField(max_length=200, blank=True,
                               verbose_name="Source Attribution", 
                               help_text="A description of the title.")
    source_link = models.URLField(blank=True, null=True)
    color = models.CharField(max_length=10, blank=True,
                             verbose_name="Header text colour")
    
    class Meta(WiqiStack.Meta):
        db_table = "image"
        verbose_name_plural = "Images"

    def set(self, **kwargs):
        # validate image and fail if it doesn't pass
        if not kwargs.get("reverted_from", False):
            assert(imghdr.what(kwargs["file"]) in ['jpg', 'jpeg', 'png', 'gif'])
            if not kwargs.get("color", None):
                self.color = dominantcolor.fontcolor(kwargs["file"])
        self.file = kwargs["file"]
        self.caption = kwargs.get("caption", "")
        self.source_attribution = kwargs.get("source_attribution", "")
        self.source_link = kwargs.get("source_link", None)
        super(Image, self).set(**kwargs)
    
    def update(self, **kwargs):
        try:
            assert(self.file == kwargs["file"])
            assert(self.caption == kwargs["caption"])
            assert(self.source_attribution == kwargs["source_attribution"])
            assert(self.source_link == kwargs["source_link"])
            super(Image, self).update(**kwargs)
            return False
        except AssertionError, e:
            new_base = Image()
            new_base.set(**kwargs)
            return new_base
        
    def revert(self, **kwargs):
        """
        Creates a new stack item copying all the content from the original but replacing with the user information of the revertor.
        """
        kwargs["file"] = self.file
        kwargs["caption"] = self.caption
        kwargs["source_attribution"] = self.source_attribution
        kwargs["source_link"] = self.source_link
        kwargs["color"] = self.color
        super(Image, self).revert(Image, **kwargs)

    @property
    def htmlresponse(self):
        return '<img src="%s">' % self.file.url
    
    @property
    def jsonresponse(self):
        return json.dumps({'image': self.htmlresponse,
                           'attribution': self.caption,
                           'imagesurl': self.wiqi.surl,
                           'imagestacksurl': self.surl,
                           'color': self.color })