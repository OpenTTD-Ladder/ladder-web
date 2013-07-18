ENABLE_DEBUG_TOOLBAR = True

DEBUG_TOOLBAR_REQUEST_PARAM = "q"
DEBUG_TOOLBAR_REQUEST_VALUE = "debug"

def has_package(pkg):
    try:
        __import__(pkg)
        return True
    except ImportError:
        return False

HAS_MEMCACHE_TOOLBAR = has_package('memcache_toolbar')
HAS_TEMPLATE_TIMINGS = has_package('template_timings_panel')

if ENABLE_DEBUG_TOOLBAR and not has_package('debug_toolbar'):
    ENABLE_DEBUG_TOOLBAR = False

def custom_show_toolbar(request):
    if not ENABLE_DEBUG_TOOLBAR:
        return False
    if not request.user.is_superuser:
        return False
    if request.POST.get(DEBUG_TOOLBAR_REQUEST_PARAM, False) == DEBUG_TOOLBAR_REQUEST_VALUE:
        request.POST = request.POST.copy()
        del request.POST['q']
        return True
    if request.GET.get(DEBUG_TOOLBAR_REQUEST_PARAM, False) == DEBUG_TOOLBAR_REQUEST_VALUE:
        request.GET = request.GET.copy()
        del request.GET['q']
        return True
    return False

if ENABLE_DEBUG_TOOLBAR:
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    )
    if HAS_MEMCACHE_TOOLBAR:
        DEBUG_TOOLBAR_PANELS += (
            'memcache_toolbar.panels.pylibmc.PylibmcPanel',
            )
    if HAS_TEMPLATE_TIMINGS:
        DEBUG_TOOLBAR_PANELS += (
            'template_timings_panel.panels.TemplateTimings.TemplateTimings',
            )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
        'HIDE_DJANGO_SQL': False,
        'TAG': 'div',
        'ENABLE_STACKTRACES' : True,
    }
else:
    DEBUG_TOOLBAR_PANELS = ()
    DEBUG_TOOLBAR_CONFIG = {}

TEMPLATE_TIMINGS_SETTINGS = {
    'PRINT_TIMINGS': False,
}
