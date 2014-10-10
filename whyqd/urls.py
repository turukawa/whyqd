from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from whyqd import settings

# from django.contrib import admin
from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('django_facebook.auth_urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^usr/', include('whyqd.usr.urls')),
    url(r'^my/', include('whyqd.novel.urls')),
    url(r'^', include('whyqd.wiqi.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
