from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

class MenuItem(object):
    layout  = None
    acl     = []
    sub     = []
    css     = None
    url     = None
    target  = None
    icon    = None
    text    = None
    attrs   = {}
    index   = 0
    template = None

    def build_url(self, user):
        url, suffix = self.url, ''
        if isinstance(url, (list, tuple)):
            url, suffix = url[:2]
        if isinstance(url, basestring) and url.startswith('::'):
            args = {}
            if isinstance(suffix, (list, dict)):
                args = {'args': (), 'kwargs': {}}
                if isinstance(suffix, list):
                    args['args'] = suffix
                else:
                    args['kwargs'] = kwargs
            url = reverse(url[2:], **args)
        return (url if url is not None else '#') + suffix
        
    def build_text(self, user):
        if self.text is None:
            return self.text
        if self.text.startswith('::'):
            return _(self.text[2:])
        return self.text
        
    def build_attrs(self, user):
        if len(self.attrs) == 0:
            return ''
        else:
            return ' '.join(['%s="%s"' % (k, v) for k, v in self.attrs.items()])
        
    def build_icon(self, user):
        if callable(self.icon):
            return self.icon(user)
        return self.icon

    def get(self, user, check):
        subitems = sorted(list(self.get_subitems(user, check)))
        return self.index, {
            'url': self.build_url(user),
            'target': self.target,
            'css': self.css,
            'text': self.build_text(user),
            'text_orig': str(self.text),
            'attrs': self.build_attrs(user),
            'attrs_orig': self.attrs,
            'icon': self.build_icon(user),
            'template': self.template,
            'sub': subitems,
        }

    def get_subitems(self, user, check):
        for item in self.sub:
            if check(item):
                yield item.get(user, check)

class Separator(MenuItem):
    text    = ''
    css     = 'divider'
    url     = ''
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
