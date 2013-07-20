INSTALLED_APPS = (
    'design',
    'util',

    'account',
    'matchmaking',

    'translations',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


from .debug_toolbar import ENABLE_DEBUG_TOOLBAR, HAS_MEMCACHE_TOOLBAR, HAS_TEMPLATE_TIMINGS

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar',
        )
    if HAS_MEMCACHE_TOOLBAR:
        INSTALLED_APPS += (
            'memcache_toolbar',
            )
    if HAS_TEMPLATE_TIMINGS:
        INSTALLED_APPS += (
            'template_timings_panel',
            )