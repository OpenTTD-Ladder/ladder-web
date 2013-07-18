import os
from django.conf import settings
from django import template
#pylint: disable=C0103
register = template.Library()

STATIC_FORMAT = {
    "css": '<link href="%s" rel="stylesheet" media="screen">\n',
    "js": '<script src="%s"></script>\n',
}

class StaticFileNode(template.Node):
    def __init__(self, static_type, static_file):
        self.static_type = static_type
        self.static_file = static_file

    def __repr__(self):
        return "<Menu Node>"

    def render(self, context):
        try:
            static_file = self.static_file
            if static_file[0] == static_file[1] and static_file[0] in ('"', "'"):
                static_file = static_file[1:-1]
            else:
                static_file = template.Variable(static_file).resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if isinstance(static_file, basestring):
            static_file = [static_file,]

        ret = ''
        minified = '.min' if not settings.DEBUG else ''
        for item in static_file:
            parts = os.path.splitext(item)
            fname = ''.join([os.path.join(settings.STATIC_URL, self.static_type, parts[0]), minified, parts[1]])
            ret += STATIC_FORMAT[self.static_type] % fname
        return ret

@register.tag
def static_file(parser, token):
    try:
        tag_name, static_type, static_file = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires 2 arguments" % token.contents.split()[0])
    if not (static_type[0] == static_type[-1] and static_type[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return StaticFileNode(static_type[1:-1], static_file)
