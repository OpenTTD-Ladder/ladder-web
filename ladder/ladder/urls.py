from django.conf.urls import patterns, include, url

from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ladder.views.home', name='home'),
    # url(r'^ladder/', include('ladder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)),)
