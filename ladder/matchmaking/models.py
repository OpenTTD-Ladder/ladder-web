from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from translations.models import Translatable, Translation
try:
    from ckeditor.fields import RichTextField
except ImportError:
    RichTextField = models.TextField

import trueskill

class Ladder(Translatable):
    max_slots       = models.PositiveIntegerField(default = 0)

    signup_start    = models.DateTimeField(blank = True, null = True)
    signup_ends     = models.DateTimeField(blank = True, null = True)

    ladder_start    = models.DateTimeField(blank = True, null = True)
    ladder_ends     = models.DateTimeField(blank = True, null = True)

    signup_confirm  = models.BooleanField(default = False)

    default_mu      = models.FloatField(default = 25.0)
    default_sigma   = models.FloatField(default = (25.0 / 3.0), help_text = "Default: 1/3rd of mu")
    default_beta    = models.FloatField(default = (25.0 / 3.0 / 2.0), help_text = "Default: half of sigma")
    default_tau     = models.FloatField(default = (25.0 / 3.0 / 100.0), help_text = "Default: 1% of sigma")
    default_draw    = models.FloatField(default = 0.01, help_text = "Estimated draw chance")

    admins          = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, null = True)

    _trueskill = None
    @property
    def trueskill(self):
        if self._trueskill is None:
            self._trueskill = trueskill.TrueSkill(
                mu                  = self.default_mu,
                sigma               = self.default_sigma,
                beta                = self.default_beta,
                tau                 = self.default_tau,
                draw_probability    = self.default_draw )
        return self._trueskill

class LadderTranslation(Translation):
    ladder          = models.ForeignKey(Ladder, related_name='translations')

    name            = models.CharField(max_length = 64)
    short_desc      = models.CharField(max_length = 255)
    long_desc       = RichTextField()
