from util.page import Page

from .models import News

class Frontpage(Page):
    template_name = "frontpage/frontpage.html"

    def get(self, request):
        news = list(News.objects.all().order_by('-authored')[:5])
        return self.render_to_response({
            'news': news,
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
