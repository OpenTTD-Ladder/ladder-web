from util.menu import MenuItem, menu, Separator
from util.acl import UserIsAuthenticated, UserIsStaff

from django.core.urlresolvers import reverse
from django.contrib.admin import site as admin_site

class AccountChangePassword(MenuItem):
    acl     = [
        UserIsAuthenticated(True),
    ]
    index   = 1
    text    = "::Change Password"
    icon    = "icon-pencil"

class AccountAdminLink(MenuItem):
    acl     = [
        UserIsAuthenticated(True),
        UserIsStaff(True),
    ]
    index   = 5
    text    = "::Admin Site"
    url     = "::admin:index"
    icon    = "icon-cogs"

class AccountLogout(MenuItem):
    acl     = [
        UserIsAuthenticated(True)
    ]
    index   = 10
    text    = "::Logout"
    icon    = "icon-off"
    url     = "::account:logout"
    
@menu.item
class AccountMenuItem(MenuItem):
    layout  = 'right'
    index   = 10
    sub     = [
        AccountChangePassword(),
        Separator(acl=[UserIsAuthenticated(True)], index=AccountChangePassword.index+1),
        AccountAdminLink(),
        Separator(acl=[UserIsAuthenticated(True), UserIsStaff(True)], index=AccountAdminLink.index+1),
        AccountLogout(),
    ]
    acl     = [
        UserIsAuthenticated(True)
    ]
    icon    = "icon-user"
    def build_text(self, user):
        return user.first_name and user.first_name or user.username

@menu.item
class AccountLogin(MenuItem):
    layout  = "right"
    acl     = [
        UserIsAuthenticated(False)
    ]
    index   = 10
    text    = "::Login"
    icon    = "icon-user"
    url     = "::account:login"



class AccountPublicSiteLink(MenuItem):
    acl     = [
        UserIsAuthenticated(True),
        UserIsStaff(True),
    ]
    index   = 5
    icon    = 'icon-globe'
    text    = '::Home'
    url     = '::index'


@menu.item
class AdminAccountMenuItem(MenuItem):
    layout  = 'admin-right'
    sub     = [
        AccountChangePassword(),
        Separator(index = AccountChangePassword.index+1),
        AccountPublicSiteLink(),
        Separator(acl=[UserIsAuthenticated(True), UserIsStaff(True)], index=AccountPublicSiteLink.index+1),
        AccountLogout(),
    ]
    acl     = [
        UserIsAuthenticated(True),
        UserIsStaff(True)
    ]
    icon    = "icon-user"
    def build_text(self, user):
        return user.first_name and user.first_name or user.username

class AdminApplicationSubMenuItem(MenuItem):
    icon    = "icon-th-list"
    def __init__(self, app_label):
        self.app_label = app_label
        self.text = app_label.capitalize()
        self.index = app_label

    def build_url(self, user):
        return reverse("admin:app_list", kwargs={'app_label': self.app_label})



@menu.item
class AdminApplicationMenuItem(MenuItem):
    layout  = 'admin-left'
    acl     = [
        UserIsAuthenticated(True),
        UserIsStaff(True)
    ]
    sub     = [
    ]
    icon    = "icon-list"
    text    = "::Applications"

    def get_subitems(self, user, check):
        class UserWrapper(object):
            def __init__(self, user):
                self.user = user
        helper = UserWrapper(user)

        apps = []

        for model, model_admin in admin_site._registry.items(): #pylint: disable=W0212
            app_label = model._meta.app_label #pylint: disable=W0212
            if app_label in apps:
                continue
            apps.append(app_label)
            has_module_perms = user.has_module_perms(app_label)
            if not has_module_perms:
                continue
            perms = model_admin.get_model_perms(helper)
            if any(perms.values()):
                yield AdminApplicationSubMenuItem(app_label).get(user, check)

        for item in self.sub:
            if check(item):
                yield item.get(user, check)