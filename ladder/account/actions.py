import logging
log = logging.getLogger(__name__)

from django.contrib.auth.hashers import UNUSABLE_PASSWORD
def disable_accounts(self, request, queryset):
    if not request.user.is_superuser:
        return
    accounts = list(queryset.all())
    for account in accounts:
        log.warning("Disabling account: %s", account.username)
        account.set_unusable_password()
        account.save()
    self.message_user(request, "%s account%s disabled" % (len(accounts), ('' if len(accounts) == 1 else 's')))
disable_accounts.short_description = "Disable selected users"
