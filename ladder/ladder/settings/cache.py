CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
    'LOCATION': '127.0.0.1:11211',
    }
}
CACHE_ENABLED           = True
CACHE_MIDDLEWARE_SECONDS = 300
SESSION_COOKIE_AGE      = 31449600
SESSION_ENGINE          = 'django.contrib.sessions.backends.cached_db'
