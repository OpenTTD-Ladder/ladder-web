AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = (
    'account.backends.ModelBackend',
)

LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
LOGIN_REDIRECT_URL = '/'