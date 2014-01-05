from django.contrib.gis import admin
from whyqd.usr.models import User #, Geomap #, Attribute, AttributeStack

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('username',)
    list_per_page = 50
    ordering = ['username']
    search_fields = ['username']
    
admin.site.register(User, UserAdmin)