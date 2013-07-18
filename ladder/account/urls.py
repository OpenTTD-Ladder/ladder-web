from django.conf.urls import patterns, url
from .views import Login, Logout

urlpatterns = patterns('',
    url(r'^login/$',       Login.as_view(),    name = 'login'),
    url(r'^logout/$',      Logout.as_view(),   name = 'logout'),
)
