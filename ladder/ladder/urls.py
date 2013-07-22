from django.conf.urls import patterns, include, url
from django.conf import settings

from util.page import TemplatePage

from frontpage.views import Frontpage

urlpatterns = patterns('',
    url(r'^$',        Frontpage.as_view(), name = "index"),
    url(r'^',         include('frontpage.urls', namespace="frontpage")),
    url(r'^account/', include('account.urls', namespace="account")),

    url(r'^ckeditor/', include('ckeditor.urls')),
)

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)),)
