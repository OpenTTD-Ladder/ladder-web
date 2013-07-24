from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from translations.models import Translatable, Translation
from translations.managers import TranslatableManager

from util.cache import cache, CACHE_MINUTE

try:
    from ckeditor.fields import RichTextField
except ImportError:
    RichTextField = models.TextField

import trueskill


class LadderManager(TranslatableManager):

    def get_ladders(self):
        active = Ladder.objects.get_active()
        signup = Ladder.objects.get_signup()
        upcoming = Ladder.objects.get_upcoming()
        return {
            'active': active,
            'signup': signup,
            'upcoming': upcoming,
        }

    def get_ladders_list(self, limit = None):
        """
        Returns the same data as `get_ladders`, but instead
        of querying on the signup/active start/end, we use
        cached pk lists, and grab only what we need.
        """

        active_pks = self.get_active_pks_cached()[:limit]
        signup_pks = self.get_signup_pks_cached()[:limit]
        upcoming_pks = self.get_upcoming_pks_cached()[:limit]

        pks_to_get = list(set(active_pks + signup_pks + upcoming_pks))

        items = dict([(x.pk, x) for x in self.get_query_set().filter(pk__in = pks_to_get)])
        return {
            'active':   [items[x] for x in active_pks],
            'signup':   [items[x] for x in signup_pks],
            'upcoming': [items[x] for x in upcoming_pks],
        }
       

    @cache
    def get_active_pks_cached(self):
        return list(self.get_active().values_list('pk', flat=True))
    get_active_pks_cached.seconds = CACHE_MINUTE * 15

    @cache
    def get_signup_pks_cached(self):
        return list(self.get_signup().values_list('pk', flat=True))
    get_signup_pks_cached.seconds = CACHE_MINUTE * 15

    @cache
    def get_upcoming_pks_cached(self):
        return list(self.get_upcoming().values_list('pk', flat=True))
    get_upcoming_pks_cached.seconds = CACHE_MINUTE * 15


    def get_active(self):
        now = timezone.now()
        qs = self.get_query_set()

        qs = qs.filter(
                Q(Q(ladder_start__isnull = True) | Q(ladder_start__lt = now)) &
                Q(Q(ladder_ends__isnull = True)  | Q(ladder_ends__gt = now))
            ).order_by('ladder_ends')
        return qs

    def get_signup(self):
        now = timezone.now()
        qs = self.get_query_set()

        qs = qs.filter(
                Q(Q(signup_start__isnull = True) | Q(signup_start__lt = now)) &
                Q(Q(signup_ends__isnull = True)  | Q(signup_ends__gt = now))
            ).order_by('signup_ends')
        return qs

    def get_upcoming(self):
        now = timezone.now()
        qs = self.get_query_set()

        qs = qs.filter(
                Q(ladder_start__isnull = False) | Q(ladder_start__gt = now)
            ).order_by('ladder_starts')
        return qs


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

    objects         = LadderManager()

    _is_active = None
    def is_active(self):
        if self._is_active is None:
            now = timezone.now()
            self._is_active = (self.ladder_start is None or (now > self.ladder_start)) and (self.ladder_ends is None or (now < self.ladder_ends))
        return self._is_active
    is_active.boolean = True

    _is_signup = None
    def is_signup(self):
        if self._is_signup is None:
            self._is_signup = (self.signup_start is not None) or (self.signup_ends is not None) or self.signup_confirm
        return self._is_signup
    is_signup.boolean = True

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

    def __unicode__(self):
        return self.name
