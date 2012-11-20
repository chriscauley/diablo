from django import forms
from django.core.mail import mail_admins

from .models import Account

import traceback

class AccountForm(forms.ModelForm):
    def save_or_none(self,*args,**kwargs):
        # pulling from diablo api fails a lot
        # API model tries to get toon three times for each url and returns False on a fail
        obj = self.save(*args,**kwargs)
        if not obj:
            Account.objects.get(hero__isnull=True).delete()
        return obj
    class Meta:
        model = Account
        fields = ("region","name","code")
