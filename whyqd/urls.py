from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# new format import, deprecating patterns
from whyqd import settings, novel, usr, wiqi
from django.contrib.staticfiles import views

# from django.contrib import admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^media/(?P<path>.*)$', views.serve),
    url(r'^admin/', admin.site.urls, name="test"),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls')),
    url(r'^usr/', include('whyqd.usr.urls')),
    url(r'^my/', include('whyqd.novel.urls')),
    # App icons
    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'),
                                               permanent=False), name="favicon"),
    url(r'^apple-touch-icon-57x57.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-57x57.png'),
        permanent=False), name="apple-touch-icon-57x57"),
    url(r'^apple-touch-icon-60x60.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-60x60.png'),
        permanent=False), name="apple-touch-icon-60x60"),
    url(r'^apple-touch-icon-72x72.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-72x72.png'),
        permanent=False), name="apple-touch-icon-72x72"),
    url(r'^apple-touch-icon-76x76.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-76x76.png'),
        permanent=False), name="apple-touch-icon-76x76"),
    url(r'^apple-touch-icon-114x114.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-114x114.png'),
        permanent=False), name="apple-touch-icon-114x114"),
    url(r'^apple-touch-icon-120x120.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-120x120.png'),
        permanent=False), name="apple-touch-icon-120x120"),
    url(r'^apple-touch-icon-144x144.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-144x144.png'),
        permanent=False), name="apple-touch-icon-144x144"),
    url(r'^apple-touch-icon-152x152.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-152x152.png'),
        permanent=False), name="apple-touch-icon-152x152"),
    url(r'^apple-touch-icon-180x180.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/apple-touch-icon-180x180.png'),
        permanent=False), name="apple-touch-icon-180x180"),
    url(r'^favicon-32x32.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/favicon-32x32.png'),
        permanent=False), name="favicon-32x32"),
    url(r'^android-chrome-192x192.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/android-chrome-192x192.png'),
        permanent=False), name="android-chrome-192x192"),
    url(r'^favicon-96x96.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/favicon-96x96.png'),
        permanent=False), name="favicon-96x96"),
    url(r'^favicon-16x16.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/favicon-16x16.png'),
        permanent=False), name="favicon-16x16"),
    url(r'^mstile-144x144.png$', RedirectView.as_view(
        url=staticfiles_storage.url('images/mstile-144x144.png'),
        permanent=False), name="mstile-144x144"),
    url(r'^manifest.json$', RedirectView.as_view(
        url=staticfiles_storage.url('js/manifest.json'),
        permanent=False), name="manifestjson"),
    url(r'^browserconfig.xml$', RedirectView.as_view(
        url=staticfiles_storage.url('js/browserconfig.xml'),
        permanent=False), name="browserconfig"),
    # End app icons
    url(r'^', include('whyqd.wiqi.urls')),
    ]

#https://docs.djangoproject.com/en/1.9/howto/static-files/#serving-static-files-during-development
if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ] + static(settings.STATIC_URL)