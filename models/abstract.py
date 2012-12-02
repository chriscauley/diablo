from django.core.mail import mail_admins
from django.db import models
from django.http import Http404

import requests, traceback
from simplejson import loads

class ModelManager(models.Manager):
    def get_or_init(self,*args,**kwargs):
        """Just like get_or_create, only it doesn't save"""
        try:
            return self.get(*args,**kwargs), False
        except self.model.DoesNotExist:
            return self.model(*args,**kwargs), True
    def get_or_none(self,*args,**kwargs):
        try:
            return self.get(*args,**kwargs)
        except self.model.DoesNotExist:
            return
    def get_or_404(self,*args,**kwargs):
        try:
            return self.get(*args,**kwargs)
        except self.model.DoesNotExist:
            raise Http404("%s matching args=%s and kwargs=%s does not exist"%(self.model.__name__,args,kwargs))
    def lazy_from_kwargs(self,**kwargs):
        """
        Does a get_or_init based on self.model._meta.unique_together.
        It then applies the rest of the dict and saves.
        Really useful for jsons.
        """
        uniques = {}
        for attr in self.model._meta.unique_together[0]:
            uniques[attr] = kwargs.pop(attr)
        obj, new = self.get_or_init(**uniques)
        for k,v in kwargs.items():
            setattr(obj,k,v)
        obj.save()
        if new:
            print "Created new %s: %s"%(self.model.__name__,obj)
        return obj

class Model(models.Model):
    objects = ModelManager()

    @property
    def admin_link(self):
        url = "/admin/diablo/%s/%s"%(self.__class__.__name__.lower(),self.pk)
        return "<a href='%s'>%s</a>"%(url,self)
    class Meta:
        abstract = True

class _Meta:
    app_label = 'diablo'

class APINotFound(Exception):
    pass

class APIModel(Model):
    """
    Model to house the abstract functions for dealing with battlenet.
    Requires a property `self.api_url` to get the info from battlenet.
    Requires a list of updates, corresponding to a "update_<update>" function on the model.
    This is used to connect update_all to the corresponding functions which process the toon.
    """
    def _get_toon(self):
        if not hasattr(self,'_toon'):
            tries = 0
            success = False
            while tries <= 3:
                tries += 1
                try:
                    r = requests.get(self.api_url)
                    self._toon = loads(r.text)
                    success = True
                    break
                except:
                    pass
            if not success:
                mail_admins("Session not found",traceback.format_exc())
                return False
            if self._toon.get('code','') == 'OOPS':
                raise APINotFound("No data exists at:%s"%self.api_url)
        return self._toon
    toon = property(_get_toon)

    def update_all(self):
        for update in self.updates:
            getattr(self,'update_'+update)()

    class Meta:
        abstract = True

    def save(self,*args,**kwargs):
        new = not self.pk
        super(Model,self).save(*args,**kwargs)
        if new:
            self.update_all()

