from django.conf.urls import patterns, include, url
from whyqd import settings

# from django.contrib import admin
from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usr/', include('whyqd.usr.urls')),
    url(r'^', include('whyqd.wiqi.urls')),
)
