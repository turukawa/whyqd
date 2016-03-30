from django.conf.urls import patterns, include, url

# Django 1.9 url patterns
from whyqd.usr import views
from django.contrib.auth import views as dviews

urlpatterns = [
    url(r'^logout/$', dviews.logout, {'next_page': '/'}, name='usr_logout'),
    ]

urlpatterns += [
    # Update user email address
    url(r"^update/", views.usr_update, name="usr_update"),
    #url(r'^subscribe/$', 'subscribe', {'template_name': 'usr/subscribe.html'}, name='subscribe'),
    #url(r'^register/$', 'register', {'template_name': 'usr/register.html'}, name='usr_register'),
    ]