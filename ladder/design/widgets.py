from django.forms.widgets import Textarea, TextInput, DateInput, TimeInput, MultiWidget
from django.forms import Media
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import AdminSplitDateTime

__all__ = [
    "Textarea",
    "Textarea",
    "TextInput",
    "IntegerInput",
    "URLInput",
    "DateInput",
    "TimeInput",
    "DateTimeInput",
]

class _Textarea(Textarea):
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'class': 'span5', 'rows': 10, 'cols': 80}
        if attrs:
            default_attrs.update(attrs)
        # NOTE: We call the Textarea (NOT the _Textarea!!!) super
        super(Textarea, self).__init__(default_attrs)
        
class _TextInput(TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input-large'}
        if attrs:
            default_attrs.update(attrs)
        super(_TextInput, self).__init__(default_attrs)
        
class _IntegerInput(TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input-small'}
        if attrs:
            default_attrs.update(attrs)
        super(_IntegerInput, self).__init__(default_attrs)
        
class _URLInput(_TextInput):
    pass

class _DateInput(DateInput):
    @property
    def media(self):
        js_files = ["calendar.js", "admin/DateTimeShortcuts.js"]
        return Media(js=[static("admin/js/%s" % path) for path in js_files])
    
    def __init__(self, attrs=None, format=None): # pylint: disable=W0622
        final_attrs = {'class': 'input-small vDateField', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(_DateInput, self).__init__(attrs=final_attrs, format=format)
        
class _TimeInput(TimeInput):
    @property
    def media(self):
        js_files = ["calendar.js", "admin/DateTimeShortcuts.js"]
        return Media(js=[static("admin/js/%s" % path) for path in js_files])

    def __init__(self, attrs=None, format=None): # pylint: disable=W0622
        final_attrs = {'class': 'input-small vTimeField', 'size': '8'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(_TimeInput, self).__init__(attrs=final_attrs, format=format)

class _DateTimeInput(AdminSplitDateTime):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None): # pylint: disable=W0231
        widgets = [_DateInput, _TimeInput]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        MultiWidget.__init__(self, widgets, attrs) # pylint: disable=W0233

Textarea        = _Textarea
TextInput       = _TextInput
IntegerInput    = _IntegerInput
URLInput        = _URLInput
DateInput       = _DateInput
TimeInput       = _TimeInput
DateTimeInput   = _DateTimeInput