from django.contrib.gis import admin
from whyqd.wiqi.models import Wiqi, Text, Image, Book#, Geomap #, Attribute, AttributeStack

class WiqiAdmin(admin.ModelAdmin):
    list_display = ('id', 'stack',)
    list_display_links = ('id',)
    list_per_page = 50
    ordering = ['id']
    search_fields = ['id']
    
admin.site.register(Wiqi, WiqiAdmin)

class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',  'word_count',)
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['title']
    search_fields = ['title']

admin.site.register(Text, TextAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image',  'source_attribution',)
    list_display_links = ('image',)
    list_per_page = 50
    ordering = ['image']
    search_fields = ['title']

admin.site.register(Image, ImageAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors',  'pitch',)
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['title']
    search_fields = ['title', 'authors', 'pitch']

admin.site.register(Book, BookAdmin)

'''
class GeomapAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',  )
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Geomap, admin.OSMGeoAdmin)
'''
#
#class AttributeAdmin(admin.ModelAdmin):
#    list_display = ('slug', 'discussion', )
#    # which of the fields in 'list_display' tuple link to admin product page
#    list_display_links = ('slug',)
#    list_per_page = 50
#    ordering = ['slug']
#    search_fields = ['slug']
#    
## registers your product model with the admin site
#admin.site.register(Attribute, AttributeAdmin)
#
#class AttributeStackAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description', )
#    # which of the fields in 'list_display' tuple link to admin product page
#    list_display_links = ('name',)
#    list_per_page = 50
#    ordering = ['name']
#    search_fields = ['name']
#    
## registers your product model with the admin site
#admin.site.register(AttributeStack, AttributeStackAdmin)