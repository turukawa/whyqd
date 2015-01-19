from django.conf.urls import patterns, include, url

urlpatterns = patterns('django.contrib.auth.views',
                       url(r'^logout/$', 'logout', {'next_page': '/'}, name='usr_logout'),
)

urlpatterns += patterns('whyqd.usr.views',
                        # Update user email address
                        url(r"^update/", "usr_update",
                            name="usr_update"),
                       #url(r'^subscribe/$', 'subscribe', {'template_name': 'usr/subscribe.html'}, name='subscribe'),
                       #url(r'^register/$', 'register', {'template_name': 'usr/register.html'}, name='usr_register'),
)