from django.contrib import admin
from translations.admin import TranslationInline

from .models import Ladder, LadderTranslation

class LadderTranslationAdmin(TranslationInline):
    model =  LadderTranslation

class LadderAdmin(admin.ModelAdmin):
    inlines = [LadderTranslationAdmin]

    fieldsets = (
        (None, {'fields': [('max_slots', 'signup_confirm'),]}),
        ('Dates', {'fields': [('ladder_start', 'ladder_ends'),]}),
        ('Signup', {'fields': [('signup_start', 'signup_ends'),]}),
        ('Rating', {'fields': [('default_mu', 'default_draw'),
                               ('default_sigma', 'default_beta'), 
                                'default_tau']})
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.pk:
            return self.readonly_fields + ('default_mu', 'default_sigma', 
                    'default_beta', 'default_tau', 'default_draw',)
        return self.readonly_fields

admin.site.register(Ladder, LadderAdmin)