from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# new format import, deprecating patterns
from whyqd import settings, wiqi
from django.contrib.staticfiles import views

# from django.contrib import admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^media/(?P<path>.*)$', views.serve),
    url(r'^admin/', admin.site.urls, name="test"),
    url('^', include('django.contrib.auth.urls')),
    url(r'^', include('whyqd.wiqi.urls')),
    ]

#https://docs.djangoproject.com/en/1.9/howto/static-files/#serving-static-files-during-development
if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ] + static(settings.STATIC_URL)