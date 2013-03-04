from django.conf.urls import patterns, include, url

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
    (r'^channels/v/(.+)/$', 'channels.views.home'),
    (r'^add/channels/v/(.+)/$', 'channels.views.addlink'),
    (r'^channels/add/$', 'channels.views.add'),
    (r'^index/$', 'core.views.index'),
    (r'^$', 'core.views.index'),
    
)
