from django.conf import settings
from django.db import models
from django.utils import timezone

from translations.models import Translatable, Translation
try:
    from ckeditor.fields import RichTextField
except ImportError:
    RichTextField = models.TextField

class News(Translatable):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "news_authored")
    authored        = models.DateTimeField(default = timezone.now)

class NewsTranslation(Translation):
    news            = models.ForeignKey(News, related_name='translations')
    title           = models.CharField(max_length = 64)
    long_desc       = RichTextField()
