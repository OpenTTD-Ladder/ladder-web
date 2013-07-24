from django.utils import timezone

from util.page import Page

from .models import News

from matchmaking.models import Ladder

class Frontpage(Page):
    template_name = "frontpage/frontpage.html"

    def get(self, request):
        news = list(News.objects.filter(authored__lte = timezone.now()).prefetch_related('author').order_by('-authored')[:5])
        return self.render_to_response({
            'news': news,
            'ladders': Ladder.objects.get_ladders_list(20),
            })

class NewsItem(Page):
    template_name = "frontpage/news.html"

    def get(self, request, id, slug):
        try:
            item = News.objects.get(pk = id)
        except (ValueError, News.DoesNotExist): 
            return self.http404()

        return self.render_to_response({
            'item': item,
            })
