from .base import BasePage, ACLPageMixin

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

import json

class AjaxResponse(HttpResponse):
    def __init__(self, request, context, content_type='application/json', status=None, template=None):
        content = json.dumps(context, cls=DjangoJSONEncoder, indent = settings.DEBUG and 2 or None)
        callback = request.GET.get('callback', None)
        if callback:
            content = '%s(%s)' % (callback, content)
        super(AjaxResponse, self).__init__(content, content_type, status)

class BaseAjaxPage(BasePage):
    _ajax_methods = ['get', 'post']
    ajax_response_class = AjaxResponse

    def _get_handler_internal(self, request, method):
        handler = method
        if (request.is_ajax() or request.GET.get('is_ajax', False)) and method in self._ajax_methods:
            handler = 'ajax_%s' % method
        return getattr(self, handler, self.http_method_not_allowed)

    def render_ajax_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', 'application/json')
        return self.ajax_response_class(
            request = self.request,
            context = context,
            **response_kwargs
            )

    def render_ajax_error_response(self, code, message):
        return self.render_ajax_response({'result': 'error', 'statuscode': code, 'statusmsg': message}, status=code)

    def http_method_not_authorized(self, request, *args, **kwargs):
        return self.render_ajax_error_response(403, 'Forbidden')

class AjaxPage(BaseAjaxPage, ACLPageMixin):
    _get_handler = ACLPageMixin._get_handler
    pass
