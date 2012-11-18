from django.contrib import admin

from diablo.models import Account

class AccountAdmin(admin.ModelAdmin):
    pass

account_tuples = [(Account,AccountAdmin)]
