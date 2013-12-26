from django.conf.urls import patterns, include, url

urlpatterns = patterns('django.contrib.auth.views',
                       (r'^logout/$', 'logout', {'next_page': '/list/'}),
)

urlpatterns += patterns('whyqd.usr.views',
                       #url(r'^subscribe/$', 'subscribe', {'template_name': 'usr/subscribe.html'}, name='subscribe'),
                       url(r'^', include('allauth.urls'), name='usr_all'),
)