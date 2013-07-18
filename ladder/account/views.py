from util.page import AjaxPage, Page
from util.acl import UserIsAuthenticated
from util.cache import cache, CACHE_SECOND
from django.shortcuts import resolve_url

from django.utils.http import base36_to_int, is_safe_url

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

from django.conf import settings
import urlparse

class Login(Page):
    acl = [
        UserIsAuthenticated(False)
    ]
    template_name = "account/login.html"
    login_url = '/'

    redirect_field_name = REDIRECT_FIELD_NAME
    authentication_form = AuthenticationForm

    def get(self, request):
        redirect_to = request.REQUEST.get(self.redirect_field_name, '')
        form = self.authentication_form(request)
        return self.render_to_response({'form': form, self.redirect_field_name: redirect_to})

    def post(self, request):
        redirect_to = request.REQUEST.get(self.redirect_field_name, '')
        form = self.authentication_form(data = request.POST)
        if form.is_valid():
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            auth_login(request, form.get_user())
            return self.redirect(url = redirect_to)
        return self.render_to_response({'form': form, self.redirect_field_name: redirect_to})

class Logout(Page):
    acl = [

    ]
    template_name = "account/logout.html"

    redirect_field_name = REDIRECT_FIELD_NAME

    def get(self, request, next_page = None):
        auth_logout(request)

        if self.redirect_field_name in request.REQUEST:
            next_page = request.REQUEST[self.redirect_field_name]
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = request.path

        if next_page:
            return self.redirect(url = next_page)
        return self.render_to_response({})

class LogoutLogin(Logout):
    def get(self, request, login_url = None):
        if not login_url:
            login_url = settings.LOGIN_URL
        return super(LogoutLogin, self).get(request, next_page = login_url)

