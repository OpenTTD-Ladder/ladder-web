import os

CURRENT_DIR             = os.path.dirname(__file__)
APP_DIR                 = os.path.dirname(CURRENT_DIR)
ROOT_DIR                = os.path.dirname(APP_DIR)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT             = os.path.join(ROOT_DIR, 'static')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT              = os.path.join(ROOT_DIR, 'media')