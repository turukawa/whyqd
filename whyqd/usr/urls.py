from django.conf.urls import patterns, include, url

urlpatterns = patterns('django.contrib.auth.views',
                       url(r'^logout/$', 'logout', {'next_page': '/list/'}, name='usr_logout'),
)

urlpatterns += patterns('whyqd.usr.views',
                       #url(r'^subscribe/$', 'subscribe', {'template_name': 'usr/subscribe.html'}, name='subscribe'),
                       #url(r'^register/$', 'register', {'template_name': 'usr/register.html'}, name='usr_register'),
)