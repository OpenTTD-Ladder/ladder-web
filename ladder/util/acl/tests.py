class BaseACLItem(object):
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset( self.__dict__.items()  + [(self.__class__,),] ))

    test_request = False
    test_user = False

class UserIsAuthenticated(BaseACLItem):
    logged_in = True

    def __init__(self, logged_in = True):
        self.logged_in = logged_in

    def test_user(self, user):
        return user.is_authenticated() == self.logged_in

class UserIsStaff(BaseACLItem):
    is_staff = True

    def __init__(self, is_staff = True):
        self.is_staff = is_staff

    def test_user(self, user):
        return user.is_staff == self.is_staff

class UserIsSuperuser(BaseACLItem):
    is_superuser = True

    def __init__(self, is_superuser = True):
        self.is_superuser = is_superuser

    def test_user(self, user):
        return user.is_superuser == self.is_superuser
        
class UserInGroup(BaseACLItem):
    group_name = None
    def __init__(self, group_name):
        self.group_name = group_name

    def test_user(self, user):
        cached = getattr(user, '_group_name_cache', None)
        if cached is None:
            cached = set(user.groups.values_list('name', flat=True))
            setattr(user, '_group_name_cache', cached)
        return self.group_name in cached

class UserHasPermission(BaseACLItem):
    permission = None
    def __init__(self, permission):
        self.permission = permission

    def test_user(self, user):
        cached = getattr(user, '_permission_cache', None)
        if cached is None:
            cached = user.get_all_permissions()
            setattr(user, '_permission_cache', cached)
        return self.permission in cached
