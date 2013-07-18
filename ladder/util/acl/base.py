from ..cache import cache
from ..loggable import LoggableObject
from django.contrib.auth import get_user_model

class ACLHandler(object):
    acl = []
    acl_cache_per_user = False

    def _test_acl_for_request(self, request):
        for item in self.acl:
            if callable(item.test_request):
                if item.test_request(request) == False:
                    return False
            else:
                if item.test_user(request.user) == False:
                    return False
        return True

    def test_acl_for_request(self, request):
        if self.acl_cache_per_user:
            return self.test_acl_for_user(request.user)
        return self._test_acl_for_request(request)

    def _test_acl_for_user(self, user):
        for item in self.acl:
            if item.test_user(user) == False:
                return False
        return True

    def test_acl_for_user(self, user):
        if self.acl_cache_per_user:
            user_model = get_user_model()
            username = getattr(user, user_model.USERNAME_FIELD)
            return self.test_acl_for_user_cached(user.is_authenticated(), username, user)
        return self._test_acl_for_user(user)

    @cache
    def test_acl_for_user_cached(self, logged_in, username, user):
        return self._test_acl_for_user(user)
    test_acl_for_user_cached.num_args = 2
    test_acl_for_user_cached.filter_kwargs = ['loggedIn', 'username']


class InvalidACLObjectException(Exception): pass

class MultiACLChecker(LoggableObject):
    def __init__(self, request = None, user = None):
        self.values = {}
        self.user = user
        self.request = request
        if user == None and request == None:
            InvalidACLObjectException("This requires either a request or user object, or both.")
        if self.user is None:
            self.user = request.user

    def check_single(self, acl):
        if acl in self.values:
            self.log.debug("check_single: cache hit: %s", acl.__class__.__name__)
            return self.values[acl]
        if self.request and callable(acl.test_request):
            self.values[acl] = ret = acl.test_request(self.request)
        else:
            self.values[acl] = ret = acl.test_user(self.user)
        return ret

    def check(self, obj):
        if not isinstance(obj, ACLHandler) and not hasattr(obj, 'acl'):
            raise InvalidACLObjectException(obj)
        return all([self.check_single(x) for x in obj.acl])

    def __call__(self, obj):
        return self.check(obj)
