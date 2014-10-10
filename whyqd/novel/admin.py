from django.contrib import admin
from whyqd.novel.models import Novel, Token

class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors',  'pitch',)
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['title']
    search_fields = ['title', 'authors', 'pitch']

admin.site.register(Novel, NovelAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ('surl', 'creator',  'novel',)
    list_display_links = ('surl',)
    list_per_page = 50
    ordering = ['surl']
    search_fields = ['creator', 'redeemer']

admin.site.register(Token, TokenAdmin)
