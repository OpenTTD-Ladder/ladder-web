from django.contrib import admin
from translations.admin import TranslationInline
from .models import News, NewsTranslation

class NewsTranslationAdmin(TranslationInline):
    model =  NewsTranslation

class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsTranslationAdmin]

admin.site.register(News, NewsAdmin)