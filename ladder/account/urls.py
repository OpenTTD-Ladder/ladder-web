from django.conf.urls import patterns, url
from .views import Login, Logout

urlpatterns = patterns('',
    url(r'^login/$',       Login.as_view(),    name = 'login'),
    url(r'^logout/$',      Logout.as_view(),   name = 'logout'),

    url(r'^password/reset/do$',  
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect': '/account/password/reset/done'}, 
        name='password_reset'),
    url(r'^password/reset/done$',  
        'django.contrib.auth.views.password_reset_done', 
        name='password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/account/password/reset/complete'},
        name='password_reset_confirm'),
    url(r'^password/reset/complete$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),
    url(r'^password/change$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/account/password/changed'},
        name='password_change'),
    url(r'^password/changed$',
        'django.contrib.auth.views.password_change_done',
        name='password_changed'),
)
