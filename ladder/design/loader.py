"""
Modified version of django's template_loader, one that does not require
applications to have a directory structure like:
  app_name/templates/app_name/file.html
but instead:
  app_name/templates/file.html
while still being 'app_name/file.html' to django.
"""

import os
import sys

from django.conf import settings
from django.utils.functional import memoize

from django.core.exceptions import ImproperlyConfigured
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join
from django.utils.importlib import import_module

# At compile time, cache the directories to search.
FS_ENCODING = sys.getfilesystemencoding() or sys.getdefaultencoding() 
APP_TEMPLATE_DIRS = []
for _app in settings.INSTALLED_APPS:
    try:
        mod = import_module(_app)
    except ImportError, error:
        raise ImproperlyConfigured('ImportError %s: %s' % (_app, error.args[0]))
    _template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    if os.path.isdir(_template_dir):
        APP_TEMPLATE_DIRS.append((_app, _template_dir.decode(FS_ENCODING)))

# It won't change, so convert it to a tuple to save memory.
APP_TEMPLATE_DIRS = tuple(APP_TEMPLATE_DIRS)


def __get_template_sources(template_name, template_dirs=None):
    return list(_get_template_sources(template_name, template_dirs))
__get_template_sources_cache = {}
_get_template_sources_cached = memoize(__get_template_sources, __get_template_sources_cache, 2)

def _get_template_sources(template_name, template_dirs=None):
    """
    Returns the absolute paths to "template_name", when appended to each
    directory in "template_dirs". Any paths that don't lie inside one of the
    template dirs are excluded from the result set, for security reasons.
    """
    if not template_dirs:
        template_dirs = APP_TEMPLATE_DIRS
    app_name = ''
    if '/' in template_name:
        app_name, template_name = template_name.split('/', 1)

    skip_apps = ('admin', 'design',)
    skip = app_name in skip_apps

    for app, template_dir in template_dirs:
        try:
            if not skip and app_name == app:
                yield safe_join(template_dir, template_name) 
            #allow index.html to be found in admin and in destiny.design, but not in other apps
            if app_name == '' and app not in skip_apps: 
                yield safe_join(template_dir, 'design', template_name)
                continue
            yield safe_join(template_dir, app_name, template_name)
        except UnicodeDecodeError:
            raise
        except ValueError:
            pass

class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        return _get_template_sources_cached(template_name, template_dirs)

    def load_template_source(self, template_name, template_dirs=None):
        paths = list(self.get_template_sources(template_name, template_dirs))
        for filepath in paths:
            try:
                fhandle = open(filepath)
                try:
                    return (fhandle.read().decode(settings.FILE_CHARSET), filepath)
                finally:
                    fhandle.close()
            except IOError:
                pass
        raise TemplateDoesNotExist(template_name)

_loader = Loader()
