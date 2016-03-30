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
from base import *
from bs4 import BeautifulSoup
from whyqd.snippets.diff2merge import mergediff

#########################################################################################################################################
# Derived Classes 
#########################################################################################################################################

class Text(WiqiStack):
    subtitle = models.CharField(max_length=500, blank=True,
                               verbose_name="Subtitle", 
                               help_text="An elaboration of the title.")
    content = models.TextField(blank=True, verbose_name="Content", 
                               help_text="Use html format to enter text.")
    custom_div = models.CharField(max_length=500, blank=True,
                                  verbose_name="Custom Div",
                                  help_text="Use html format to enter text.")
    word_count = models.IntegerField(blank=True, null=True)
    
    class Meta(WiqiStack.Meta):
        db_table = "text"
        verbose_name_plural = "Texts"
    
    def set(self, **kwargs):
        if not kwargs.get("set", False):
            kwargs = self.preprocess(**kwargs)
        self.subtitle = kwargs["subtitle"]
        self.content = kwargs["content"]
        self.word_count = 0
        if self.content:
            words = BeautifulSoup(self.content).get_text()
            self.word_count = len(words.split())
        super(Text, self).set(**kwargs)
        self.postprocess(**kwargs)
    
    def update(self, **kwargs):
        # When we branch the Wiqi, we don't want to change the stack content.
        if not kwargs.get("set", False):
            kwargs = self.preprocess(**kwargs)
        try:
            assert(self.subtitle == kwargs.get("subtitle",""))
            assert(self.content == kwargs.get("content", ""))
            super(Text, self).update(**kwargs)
            return False
        except AssertionError:
            new_base = self.copy(**kwargs)
            new_base.set(**kwargs)
            return new_base

    def preprocess(self, **kwargs):
        kwargs = super(Text, self).preprocess(**kwargs)
        kwargs["subtitle"] = BeautifulSoup(kwargs.get("subtitle","")[:500]).get_text().strip()
        kwargs["content"] = mergediff(kwargs.get("content", ""))
        kwargs["set"] = True
        return kwargs
    
    def postprocess(self, **kwargs):
        jsonset = {'url': self.get_absolute_url(),
                   'wiqiurl': self.get_url(),
                   'content': self.content,
                   'title': self.title,
                   'subtitle': self.subtitle,
                   }
        if not self.jsonresponse:
            self.jsonresponse = jsonset
        else:
            self.jsonresponse.update(jsonset)
        self.save()
  
    def revert(self, **kwargs):
        """
        Creates a new stack item copying all the content from the original but 
        replacing with the user information of the revertor.
        """
        kwargs["subtitle"] = self.subtitle
        kwargs["content"] = self.content
        kwargs["word_count"] = self.word_count
        super(Text, self).revert(Text, **kwargs)

    @property
    def htmlresponse(self):
        return self.content