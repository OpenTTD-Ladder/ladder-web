from django import http
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template.context import Context, RequestContext
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin

from ..acl import ACLHandler
from ..loggable import LoggableObject

import urllib
import urlparse

class BaseResponse(TemplateResponse):
    def __init__(self, request, template, context=None, content_type=None,
            status=None, mimetype=None, current_app=None, page = None):
        self._page = page
        super(BaseResponse, self).__init__(request, 
            template, context, content_type, status, mimetype)

    def resolve_context(self, context):
        if isinstance(context, Context):
            return context

        def _processor(request):
            return dict([(i, getattr(self._page, i, None)) for i in self._page.static_values])
        return RequestContext(self._request, context, processors=(_processor,), current_app = self._current_app)   

class BasePage(View, TemplateResponseMixin, ContextMixin, LoggableObject):
    response_class = BaseResponse

    static_values = [
        'page_css',
        'page_js',
    ]

    def __init__(self, **kwargs):
        super(BasePage, self).__init__(**kwargs)

    page_css = []
    page_js  = []

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('page', self)
        response_kwargs.setdefault('template', self.get_template_names())
        return self.response_class(
            request = self.request,
            context = context,
            **response_kwargs
            )

    def content_to_response(self, content, **response_kwargs):
        return HttpResponse(content, **response_kwargs)

    def _get_handler_internal(self, request, method):
        return getattr(self, method, self.http_method_not_allowed)
    def _get_handler(self, request, method):
        return self._get_handler_internal(request, method)

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = self._get_handler(request, request.method.lower())
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

class ACLPageMixin(ACLHandler):
    login_url = None
    def _get_handler(self, request, method):
        handler = self._get_handler_internal(request, method)
        if handler == self.http_method_not_allowed:
            return handler

        if self.test_acl_for_request(request):
            return handler
        return self.http_method_not_authorized

    def http_method_not_authorized(self, request, *args, **kwargs):
        path = request.build_absolute_uri()
        print self.login_url
        login_scheme, login_netloc = urlparse.urlparse(self.login_url or settings.LOGIN_URL)[:2]
        current_scheme, current_netloc = urlparse.urlparse(path)[:2]
        if ((not login_scheme or login_scheme == current_scheme) and 
            (not login_netloc or login_netloc == current_netloc)):
            path = request.get_full_path()
        return redirect_to_login(path, self.login_url or settings.LOGIN_URL)

    def Http404(self):
        raise http.Http404

    def redirect(self, url, query = None):
        query_bit = None
        if isinstance(query, dict):
            query_bit = urllib.urlencode(query)
        elif isinstance(query, basestring):
            query_bit = query
        if query_bit:
            url = "%s%s%s" % (url, '&' if '?' in url else '?', query_bit)
        return http.HttpResponseRedirect(url)

    def reverse(self, view, *args, **kwargs):
        return reverse(view, args = args, kwargs = kwargs)

    def redirect_reverse(self, view, *args, **kwargs):
        query = kwargs.pop('_query', None)
        url = self.reverse(view, *args, **kwargs)
        return self.redirect(url, query)

class Page(BasePage, ACLPageMixin):
    _get_handler = ACLPageMixin._get_handler

class TemplatePage(Page):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
