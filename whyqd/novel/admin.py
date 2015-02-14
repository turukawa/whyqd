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
    list_display = ('created_on', 'surl', 'stripe_id', 'creator', 'recipient', 'is_valid', 'is_purchased', 'price')
    list_display_links = ('surl',)
    list_per_page = 50
    ordering = ['created_on', 'stripe_id', 'creator', 'recipient', 'is_valid', 'is_purchased', 'price']
    search_fields = ['creator', 'redeemer', 'stripe_id']

admin.site.register(Token, TokenAdmin)
