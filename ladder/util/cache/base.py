from datetime import datetime, timedelta

from django.db import models

import logging
from .constants import CACHE_DEFAULT, CACHE_INVALIDATED_HOLDER

from hashlib import sha1

#pylint: disable=C0103
encodekey = lambda *args: '.'.join([str(x) for x in args]) 
decodekey = lambda key: key.split('.')

encodeargs = lambda *args: sha1(repr(args)).hexdigest()

def MODEL_PK(self, func):
    return self.pk

def OBJECT_PROP(kw):
    def OBJECT_PROP_GETTER(self, func):
        return getattr(self, kw, None)
    return OBJECT_PROP_GETTER

class BaseCache(object):
    # defaults
    seconds = CACHE_DEFAULT
    ignore_result = None
    use_internal = False
    num_args = None
    filter_kwargs = None
    disabled = False
    extra_key = None

    @property
    def log(self):
        log = getattr(self, '_logger', None)
        if log is None:
            log = self._logger = logging.getLogger("%s.%s" % (self.module_path, self.func_path))
        return log

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __repr__(self):
        return repr(self.func)

    def __str__(self):
        return str(self.func)

    def __get__(self, instance, cls):
        self._instance = instance
        self._cls = cls
        return self

    def get_cls(self):
        cls = getattr(self, '_cls', None)
        instance = getattr(self, '_instance', None)
        if cls is None:
            if instance is not None:
                cls = instance.__class__
            else:
                cls = getattr(self.func, '__module__', None) or '__console__'
        if isinstance(instance, models.Manager):
            cls = self._instance.model
        return cls

    def get_key_parts(self):
        cls = self.get_cls()
        ret = []
        if isinstance(cls, basestring):
            ret = [cls, self.func.__name__]
        else:
            ret = [cls.__module__, cls.__name__, self.func.__name__]
        if self.extra_key != None:
            extra = self.extra_key
            if callable(self.extra_key):
                instance = getattr(self, '_instance', None)
                extra = self.extra_key(instance, self.func)
            ret.append(extra)
        return ret

    @property
    def module_path(self):
        path = getattr(self, "_module_path", None)
        if path is None:
            path = self.get_cls()
            if not isinstance(path, basestring):
                path = path.__module__
            self._module_path = path
        return path

    @property
    def func_path(self):
        path = getattr(self, "_func_path", None)
        if path is None:
            cls = self.get_cls()
            if not isinstance(cls, basestring):
                cls = cls.__name__
            path = self._func_path = '%s.%s' % (cls, self.func.__name__)
        return path

    def get_args(self, args, kwargs):
        key_args = None
        key_kwargs = None
        if self.num_args:
            key_args = args[:self.num_args]
        else:
            key_args = args[:]
        if self.filter_kwargs:
            key_kwargs = sorted([(x, y) for x, y in kwargs.items() if x in self.filter_kwargs])
        else:
            key_kwargs = sorted(kwargs.items())
        return key_args, key_kwargs

    def get_seconds(self):
        secs = self.seconds or CACHE_DEFAULT
        if callable(secs):
            secs = secs()
        return secs

    def get_key(self, args, kwargs):
        key = encodeargs(self.get_args(args, kwargs))
        key_parts = list(self.get_key_parts())
        cache_key = encodekey(*(key_parts + [key,]))[:220]
        self.log.debug("key: %s", key)
        return cache_key

    def __call__(self, *args, **kwargs):
        from django.core.cache import cache as _djcache
        
        if self.use_internal:
            if getattr(self, '_int_cache', datetime.min) >= datetime.now():
                self.log.debug("Internal cache hit")
                return getattr(self, '_int_cache_data')

        cache_key = self.get_key(args, kwargs)

        value = _djcache.get(cache_key, None)
        if value not in (None, CACHE_INVALIDATED_HOLDER, self.ignore_result):
            self.log.debug("Cache HIT")
            return value

        self.log.debug("Cache MISS")

        return self.get_and_store(cache_key, args, kwargs)

    def get_and_store(self, cache_key, args, kwargs):
        from django.core.cache import cache as _djcache
        instance = getattr(self, '_instance', None)
        if instance is None:
            data = self.func(*args, **kwargs)
        else:
            data = self.func(instance, *args, **kwargs)
        if isinstance(data, basestring):
            if len(data) > 2**20:
                return data

        if data not in (None, CACHE_INVALIDATED_HOLDER, self.ignore_result):
            self.log.debug("Storing to cache")
            seconds = self.get_seconds()
            if self.use_internal:
                self._int_cache = datetime.now() + timedelta(seconds = seconds)
                self._int_cache_data = data
            _djcache.set(cache_key, data, seconds)
        return data  

    def force_miss(self, *args, **kwargs):
        self.log.debug("Forced MISS")
        key = encodeargs(self.get_args(args, kwargs))
        key_parts = list(self.get_key_parts())
        cache_key = encodekey(key_parts + [key,])[:220]
        self.log.debug("key: %s", key)
        return self.get_and_store(cache_key, args, kwargs)

    def invalidate(self, *args, **kwargs):
        from django.core.cache import cache as _djcache
        self.log.debug("Invalidate")
        cache_key = self.get_key(args, kwargs)
        _djcache.set(cache_key, CACHE_INVALIDATED_HOLDER, 1)
        self._int_cache = datetime.min

cache = BaseCache