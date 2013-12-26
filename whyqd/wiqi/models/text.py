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
from bs4 import BeautifulSoup

#########################################################################################################################################
# Derived Classes 
#########################################################################################################################################

class Text(WiqiStack):
    subtitle = models.CharField(max_length=500, blank=True,
                               verbose_name="Title Description", 
                               help_text="A description of the title.")
    content = models.TextField(blank=True, verbose_name="Content", 
                               help_text="Use html format to enter text.")
    word_count = models.IntegerField(blank=True, null=True)
    header_image_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_ header_image", null=True)
    header_image_object_id = models.PositiveIntegerField(null=True)
    header_image = generic.GenericForeignKey("header_image_content_type", "header_image_object_id")
    
    class Meta(WiqiStack.Meta):
        db_table = "text"
        verbose_name_plural = "Texts"
    
    def set(self, **kwargs):
        self.subtitle = kwargs.get("subtitle","")
        self.content = kwargs.get("content", "")
        self.header_image = kwargs.get("linked_wiqi_object", None)
        if self.content:
            words = BeautifulSoup(self.content).get_text()
            self.word_count = len(words.split())
        super(Text, self).set(**kwargs)
    
    def update(self, **kwargs):
        try:
            assert(self.subtitle == kwargs.get("subtitle",""))
            assert(self.content == kwargs["content"])
            if kwargs.get("linked_wiqi_object", False):
                assert(self.header_image == kwargs["linked_wiqi_object"])
            super(Text, self).update(**kwargs)
            return False
        except AssertionError:
            new_base = Text()
            new_base.set(**kwargs)
            return new_base
        
    def copy(self):
        """
        Provide a deep copy of itself for use in forks
        https://docs.djangoproject.com/en/1.5/topics/db/queries/
        If new related objects created (other than default), inherit this class.
        """
        copy_wiqi = self.wiqi
        copy_reverted_from = self.reverted_from
        copy_header_image = self.header_image
        self.pk = None
        self.id = None
        self.save()
        self.header_image = copy_header_image
        self.wiqi = copy_wiqi
        self.reverted_from = copy_reverted_from
        self.save()
        return self
        
    def revert(self, **kwargs):
        """
        Creates a new stack item copying all the content from the original but replacing with the user information of the revertor.
        """
        kwargs["subtitle"] = self.subtitle
        kwargs["content"] = self.content
        kwargs["word_count"] = self.word_count
        kwargs["linked_wiqi_object"] = self.header_image
        super(Text, self).revert(Text, **kwargs)

    @property
    def htmlresponse(self):
        return self.content
    
    @property
    def jsonresponse(self):
        try:
            header_image_jsonresponse = self.header_image.jsonresponse
        except AttributeError, e:
            header_image_jsonresponse = json.dumps({'image': None,
                                                    'attribution': None,
                                                    'imagesurl': None,
                                                    'imagestacksurl': None,
                                                    'color': 'black'})
        response = {'content': self.content, 
                    'title': self.title,
                    'subtitle': self.subtitle, 
                    'textsurl': self.surl}
        response.update(json.loads(header_image_jsonresponse))
        return json.dumps(response)