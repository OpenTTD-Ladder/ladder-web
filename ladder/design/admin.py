from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.utils.translation import ugettext

from widgets import Textarea, TextInput, IntegerInput, URLInput, DateInput, TimeInput

OVERRIDES = {
        models.TextField:       {'widget': Textarea},       # Textareas area 
        models.CharField:       {'widget': TextInput},
        models.IntegerField:    {'widget': IntegerInput},
        models.URLField:        {'widget': URLInput},
        models.DateField:       {'widget': DateInput},
        models.TimeField:       {'widget': TimeInput},
    }

class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = OVERRIDES
    
class TabularInline(admin.TabularInline):
    formfield_overrides = OVERRIDES
    
class StackedInline(admin.StackedInline):
    formfield_overrides = OVERRIDES
        
admin.ModelAdmin = ModelAdmin
admin.TabularInline = TabularInline
admin.StackedInline = StackedInline

AdminFileWidget.initial_text = ugettext('Currently')
AdminFileWidget.input_text = ugettext('Change')
AdminFileWidget.clear_checkbox_label = ugettext('Clear')
AdminFileWidget.template_with_clear = """
<li><label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s: %(clear)s</label></li>"""
AdminFileWidget.template_with_initial = """
<ul class="file-upload">
<li>%(initial_text)s: %(initial)s</li>
%(clear_template)s
<li>%(input_text)s: %(input)s</li>
</ul>"""
