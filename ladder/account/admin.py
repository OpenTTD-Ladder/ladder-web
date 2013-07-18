from django.contrib.auth.admin import UserAdmin
from .actions import disable_accounts

UserAdmin.actions += [disable_accounts]