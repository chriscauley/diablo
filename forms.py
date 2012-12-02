from django import forms
from django.core.mail import mail_admins

from .models import Account, APINotFound

import traceback

class AccountForm(forms.ModelForm):
    def clean(self,*args,**kwargs):
        cleaned_data = super(AccountForm,self).clean(*args,**kwargs)
        try:
            Account.verify(name=cleaned_data['name'],region=cleaned_data['region'],code=cleaned_data['code'])
        except APINotFound:
            raise forms.ValidationError("Unable to find account. Check info and try again.")
        return cleaned_data
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
