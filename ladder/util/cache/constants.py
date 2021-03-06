from django.conf import settings

CACHE_ENABLED = getattr(settings, 'CACHE_ENABLED', False)
CACHE_INVALIDATED_HOLDER = 'CACHE_INVALIDATED'*3


CACHE_SECOND    = 1
CACHE_MINUTE    = CACHE_SECOND * 60
CACHE_HOUR      = CACHE_MINUTE * 60
CACHE_DAY       = CACHE_HOUR   * 24

CACHE_DEFAULT   = CACHE_MINUTE * 15
