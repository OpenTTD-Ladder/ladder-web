from django.contrib.auth import backends

class ModelBackend(backends.ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = backends.get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get(**{"%s__iexact" % UserModel.USERNAME_FIELD: username})
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
