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

from olwidget.widgets import Map, EditableLayer, InfoLayer, InfoMap

#########################################################################################################################################
# Derived Classes 
#########################################################################################################################################


class Geomap(WiqiStack):
    """
    Regular Django fields corresponding to the attributes in the world borders shapefile.   
    """
    area = models.IntegerField(blank=True, null=True)
    fips = models.CharField(blank=True, verbose_name="FIPS Code", max_length=2)
    iso2 = models.CharField(blank=True, verbose_name="2 Digit ISO", max_length=2)
    iso3 = models.CharField(blank=True, verbose_name="3 Digit ISO", max_length=3)
    un = models.IntegerField(blank=True, null=True, verbose_name="United Nations Code", help_text="Use Markdown format to enter text.")
    region = models.IntegerField(blank=True, null=True, verbose_name="Region Code")
    subregion = models.IntegerField(blank=True, null=True, verbose_name="Sub-Region Code")
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    # GeoDjango-specific
    #map_marker = models.PointField(blank=True, null=True, geography=True)
    map_shape = models.MultiPolygonField(blank=True, null=True) #boundary 
    
    class Meta(WiqiStack.Meta):
        db_table = "geomap"
        verbose_name_plural = "Geomaps"
    
    def set(self, **kwargs):
        self.map_shape = kwargs["map_shape"]
        #self.html = markdown.markdown(kwargs["markup"], output_format="html5")
        super(Geomap, self).set(**kwargs)
        self.save()
    
    def update(self, **kwargs):
        try:
            assert(self.map_shape == kwargs["map_shape"])
            super(Geomap, self).update(**kwargs)
            return False
        except AssertionError, e:
            new_base = Geomap()
            new_base.set(**kwargs)
            return new_base
        
    def revert(self, **kwargs):
        """
        Creates a new stack item copying all the content from the original but replacing with the user information of the revertor.
        """
        kwargs["map_shape"] = self.map_shape
        super(Geomap, self).revert(Geomap, **kwargs)
        
    @property
    def show_map(self):
        info = [(self.map_shape, {'style': {'fill_color': 'blue'}})]
        options = {'height': "250px"}
        return InfoMap(info, options)

    @property
    def htmlresponse(self):
        return self.show_map