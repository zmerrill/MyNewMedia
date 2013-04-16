from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyNewMedia.views.home', name='home'),
    # url(r'^MyNewMedia/', include('MyNewMedia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^channels/add/$', 'channels.views.add'),
    (r'^channels/edit/(.+)$', 'channels.views.edit'),
    (r'^channels/v/(.+)/$', 'channels.views.channelhome'),
    (r'^artist/v/(.+)/$', 'channels.views.artisthome'),
    (r'^add/channels/v/(.+)/$', 'channels.views.addlink'),
    (r'^delete/channels/v/(.+)/$', 'channels.views.deletechannel'),
    (r'^subscribe/channels/v/(.+)/$', 'subscriptions.views.subscribe'),
    (r'^unsubscribe/channels/v/(.+)/$', 'subscriptions.views.unsubscribe'),
    (r'^results/$', 'search.views.results'),
    (r'^index/$', 'core.views.index'),
    (r'^$', 'core.views.index'),
    (r'^subscriptions/$', 'core.views.index'),
    (r'^channels/$', 'core.views.mychannels'),
    (r'^profile/$', 'profiles.views.profile'),
    (r'^messages/$', 'core.views.mymessages'),
    (r'^count/', include('django_counter.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^browse/$', 'channels.views.browsechannels'),
    (r'^feedpull/(.+)/$', 'channels.views.ajaxFeedPull'),
    (r'^markasread/(.+)/(.+)/$', 'channels.views.MarkAsRead'),
)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
