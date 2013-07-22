from django.conf.urls import patterns, include, url

from frontpage.views import Frontpage, NewsItem

urlpatterns = patterns('',
    url(r'^news/(?P<id>[0-9]+)/(?P<slug>[-\w]+)$', NewsItem.as_view(), name="news-item"),
)
