from django import template
#pylint: disable=C0103
register = template.Library()

from ..menu import menu
from ..cache import cache, CACHE_DAY

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_save, sender=User)
def user_saved(sender, **kwargs):
    invalidate_menu(sender.username)

@receiver(user_logged_in)
def user_logged_in(sender, request, user, **kwargs):
    invalidate_menu(user.username)

def invalidate_menu(username):
    node = MenuNode(None, None)
    for layout in menu.keys():
        node.render_for_user.invalidate(username, layout, None)

class MenuNode(template.Node):
    def __init__(self, layout, extra_css):
        self.layout = layout
        self.extra_css = extra_css

    def __repr__(self):
        return "<Menu Node>"

    @cache
    def render_for_user(self, username, layout, extra_css, request):
        layout = menu.get_layout(layout, request.user)
        tpl = template.loader.get_template('menu_list.html')
        return tpl.render(template.RequestContext(request, {'menu': layout, 'extra_css': extra_css}))
    render_for_user.num_args = 2
    render_for_user.seconds = CACHE_DAY * 3

    def render(self, context):
        try:
            request = template.Variable('request').resolve(context)
        except template.VariableDoesNotExist:
            return ''
        try:
            extra_css = self.extra_css
            if extra_css[0] == extra_css[-1] and extra_css[0] in ('"', "'"):
                extra_css = extra_css[1:-1]
            else:
                extra_css = template.Variable(extra_css).resolve(context)
        except template.VariableDoesNotExist:
            extra_css = ''
        return self.render_for_user(request.user.username if request.user.is_authenticated else None,
                                    self.layout, extra_css, request)


        layout = menu.get_layout(self.layout, request.user)       
        tpl = template.loader.get_template('menu_list.html')
        return tpl.render(template.RequestContext(request, {'menu': layout, 'extra_css': extra_css}))

@register.tag
def show_menu(parser, token):
    try:
        extra_css = ''
        tokens = token.split_contents()
        tag_name, layout = tokens[:2]
        if len(tokens) > 2:
            extra_css = tokens[2]
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (layout[0] == layout[-1] and layout[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    if len(extra_css) > 0 and not (extra_css[0] == extra_css[-1] and extra_css[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return MenuNode(layout[1:-1], extra_css)

class MenuItemNode(template.Node):
    def __init__(self, menu_item):
        self.menu_item = template.Variable(menu_item)

    def __repr__(self):
        return "<MenuItem Node>"

    def render(self, context):
        try:
            request = template.Variable('request').resolve(context)
        except template.VariableDoesNotExist:
            return ''
        try:
            level = template.Variable('menulevel').resolve(context)
            level += 1
        except template.VariableDoesNotExist:
            level = 0

        menu_item = self.menu_item.resolve(context)
        menu_item['menulevel'] = level
        if menu_item.get('template'):
            tpl = template.loader.get_template(menu_item['template'])
            return tpl.render(template.RequestContext(request, menu_item))
        else:
            tpl = template.loader.get_template('menu_item.html')
            return tpl.render(template.RequestContext(request, menu_item))

@register.tag
def render_menu_item(parser, token):
    try:
        tag_name, menu_item = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return MenuItemNode(menu_item)
