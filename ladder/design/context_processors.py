import importlib
from django.conf import settings
from django.utils.functional import memoize

APP_FORMAT = getattr(settings, "GLOBAL_STATIC_MODULE_FORMAT", "%s.static")
JS_PROPERTY = getattr(settings, "GLOBAL_STATIC_JS_PROPERTY", "global_js")
CSS_PROPERTY = getattr(settings, "GLOBAL_STATIC_CSS_PROPERTY", "global_css")

_get_global_js_files_cache = {}
def _get_global_js_files():
    files = []
    for app in settings.INSTALLED_APPS:
        try:
            module = importlib.import_module(APP_FORMAT % app)
        except ImportError:
            continue
        appfiles = getattr(module, JS_PROPERTY, [])
        if appfiles:
            files += appfiles
    return files
get_global_js_files = memoize(_get_global_js_files, _get_global_js_files_cache, 0) # pylint: disable=C0103

_get_global_css_files_cache = {}
def _get_global_css_files():
    files = []
    for app in settings.INSTALLED_APPS:
        try:
            module = importlib.import_module(APP_FORMAT % app)
        except ImportError:
            continue
        appfiles = getattr(module, CSS_PROPERTY, [])
        if appfiles:
            files += appfiles
    return files
get_global_css_files = memoize(_get_global_css_files, _get_global_css_files_cache, 0) # pylint: disable=C0103

def global_static(request):
    global_js = [y for _, y in sorted(get_global_js_files())]
    global_css = [y for _, y in sorted(get_global_css_files())]
    return {
        'global_js': global_js,
        'global_css': global_css,
    }
