from ..loggable import LoggableObject
from ..acl import MultiACLChecker
import importlib
from django.conf import settings

class InvalidMenuItem(Exception):
    pass

class BaseMenu(LoggableObject):
    def __init__(self):
        self.registered = False
        self._layouts = {}

    def item(self, section=None, compile_function=None):
        if section is None and compile_function is None:
            self.log.debug('@menu.item()')
            # @menu.item()
            return self.item_function
        elif section is not None and compile_function is None:
            if callable(section):
                self.log.debug('@menu.item')
                # @menu.item
                return self.item_function(section)
            else:
                self.log.debug('@menu.item(section) or @menu.item(section=section)')
                # @menu.item('section') or @menu.item(section='section')
                def dec(func):
                    return self.item(section, func)
                return dec
        elif section is not None and compile_function is not None:
            self.log.debug('@menu.item(section, func)')
            # menu.item('section', func)
            self._layouts[section] = self._layouts.get(section, []) + [compile_function(),]
            self.log.debug("Registering menu item to layout: %s :: %s", section, compile_function.__name__)
            return compile_function
        else:
            raise InvalidMenuItem("Unsupported argument to .item: (%r, %r)", (section, compile_function))

    def item_function(self, func):
        section = getattr(func, 'layout')
        self._layouts[section] = self._layouts.get(section, []) + [func(),]
        self.log.debug("Registering menu item to layout: %s :: %s", section, func.__name__)
        return func

    def keys(self):
        self._check_registry()
        return [unicode(x) for x in self._layouts.keys()]

    def _check_registry(self):
        if self.registered:
            return
        self.registered = True
        for app in settings.INSTALLED_APPS:
            try:
                importlib.import_module('%s.menu' % app)
            except ImportError:
                pass

    def get_layout(self, name, user):
        self._check_registry()
        check = MultiACLChecker(user = user)
        ret = []
        for menuitem in self._layouts.get(name, []):
            if not check(menuitem):
                continue
            ret.append(menuitem.get(user, check))
        return sorted(ret)

menu = BaseMenu() #pylint: disable=C0103
