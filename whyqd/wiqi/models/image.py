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
    image = models.ImageField(upload_to=get_filename, blank=True)
    caption = models.CharField(max_length=200, blank=True,
                               verbose_name="Caption", 
                               help_text="A caption for the image.")
    source_attribution = models.CharField(max_length=200, blank=True,
                               verbose_name="Source Attribution", 
                               help_text="A description of the title.")
    color = models.CharField(max_length=10, blank=True,
                             verbose_name="Header text colour")
    
    class Meta(WiqiStack.Meta):
        db_table = "image"
        verbose_name_plural = "Images"

    def set(self, **kwargs):
        # validate image and fail if it doesn't pass
        if not kwargs.get("set", False):
            kwargs = self.preprocess(**kwargs)
        self.image = kwargs["file"]
        self.caption = kwargs.get("caption", "")[:200]
        self.source_attribution = kwargs.get("source_attribution", "")[:200]
        if not kwargs.get("color", None):
            self.color = dominantcolor.fontcolor(kwargs["file"])
        else:
            self.color = kwargs["color"]
        self.jsonresponse = {'url': self.get_absolute_url(),
                             'wiqiurl': self.get_url(),
                             'image': self.htmlresponse,
                             'attribution': self.source_attribution,
                             'color': self.color
                             }
        super(Image, self).set(**kwargs)
    
    def update(self, **kwargs):
        if not kwargs.get("set", False):
            kwargs = self.preprocess(**kwargs)
        # When we branch the Wiqi, we don't want to change the stack content.
        try:
            #http://stackoverflow.com/a/9422160
            if self.image:
                assert(self.image.read() == kwargs["file"])
            else:
                assert(self.image == kwargs["file"])
            assert(self.caption == kwargs.get("caption", ""))[:200]
            assert(self.source_attribution == kwargs.get("source_attribution", ""))[:200]
            super(Image, self).update(**kwargs)
            return False
        except AssertionError:
            new_base = self.copy(**kwargs)
            new_base.set(**kwargs)
            return new_base
    
    def preprocess(self, **kwargs):
        kwargs = super(Image, self).preprocess(**kwargs)
        if not kwargs.get("reverted_from", False):
            if kwargs["file"]:
                assert(imghdr.what(kwargs["file"]) in ['jpg', 'jpeg', 'png', 'gif'])
            else:
                kwargs["file"] = self.image
                kwargs["color"] = self.color
        return kwargs
        
    def revert(self, **kwargs):
        """
        Creates a new stack item copying all the content from the original but replacing with the user information of the revertor.
        """
        kwargs["file"] = self.image
        kwargs["caption"] = self.caption
        kwargs["source_attribution"] = self.source_attribution
        kwargs["color"] = self.color
        super(Image, self).revert(Image, **kwargs)

    @property
    def htmlresponse(self):
        if self.image:
            return '<img src="%s">' % self.image.url
        return None