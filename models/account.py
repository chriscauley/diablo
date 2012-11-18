from django.contrib.auth.models import User
from django.db import models

from diablo import var
from .abstract import APIModel, _Meta, ModelManager, Model

class Region(Model):
    name = models.CharField(max_length=16)
    code = models.CharField(max_length=4)
    class Meta(_Meta):
        pass

class Account(APIModel):
    __unicode__ = lambda self: "%s#%s"%(self.name,self.code)
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User,null=True,blank=True,related_name='diablo_accounts')
    region = models.ForeignKey(Region)
    code = models.IntegerField()

    lastHeroPlayed = models.IntegerField(default=0)
    lastUpdated = models.IntegerField(default=0)

    api_url = property(lambda self: 'http://%s.battle.net/api/d3/profile/%s-%s/'%(self.region.code,self.name,self.code))
    def empty_tabs(self):
        if self.hero_set.count() > 11:
            return
        return range(11-self.hero_set.count())

    class Meta(_Meta):
        pass

    @classmethod
    def create(clss,name='',region='',code=0):
        r,new = Region.objects.get_or_create(code=region,defaults={'name':code})
        obj,new = clss.objects.get_or_create(name=name,region=r,code=code)
        obj.save()
        return obj

    updates = ['basics','artisans','progressions','heroes']

    def update_basics(self):
        self.lastHeroPlayed = self.toon['lastHeroPlayed']
        self.lastUpdated = self.toon['lastUpdated']
        self.save()
        # all this next line does is replace '-' with '' in the kills dict keys
        kills_json = dict([(k.replace('-',''),v) for k,v in self.toon['kills'].items()])
        kills = Kills.objects.lazy_from_kwargs(account=self,**kills_json)
        time = TimePlayed.objects.lazy_from_kwargs(account=self,**self.toon['timePlayed'])

    def update_artisans(self):
        for json in self.toon['artisans']:
            slug = json.pop('slug')
            d = dict(slug=slug,account=self,hardcore=False,defaults=json)
            Artisan.objects.get_or_create(**d)
        for json in self.toon['hardcoreArtisans']:
            slug = json.pop('slug')
            d = dict(slug=slug,account=self,hardcore=True,defaults=json)
            Artisan.objects.get_or_create(**d)

    def update_progressions(self):
        from .progress import Progression
        for diff, json in self.toon['progression'].items():
            uniques = {
                'difficulty': diff,
                'account': self,
                'hardcore': False,
                }
            progression = Progression.from_json(uniques,json)
        for diff, json in self.toon['hardcoreProgression'].items():
            uniques = {
                'difficulty': diff,
                'account': self,
                'hardcore': True,
                }
            progression = Progression.from_json(uniques,json)

    def update_heroes(self):
        from .hero import Hero
        for json in self.toon['heroes']:
            hero = Hero.objects.lazy_from_kwargs(account=self,**json)
            hero.update_all()

class UniqueAccountModel(Model):
    account = models.OneToOneField(Account)
    __unicode__ = lambda self: "%s - %s"%(self.__class__.__name__,self.account)
    class Meta(_Meta):
        abstract = True

class AccountModel(Model):
    account = models.ForeignKey(Account)
    __unicode__ = lambda self: "%s - %s"%(self.__class__.__name__,self.account)
    class Meta(_Meta):
        abstract = True

class Kills(UniqueAccountModel):
    monsters = models.IntegerField()
    elites = models.IntegerField()
    hardcoreMonsters = models.IntegerField()
    class Meta(_Meta):
        unique_together = ('account',)

class TimePlayed(UniqueAccountModel):
    barbarian = models.FloatField(default=0)
    demonhunter = models.FloatField(default=0)
    monk = models.FloatField(default=0)
    witchdoctor = models.FloatField(default=0)
    wizard = models.FloatField(default=0)
    class Meta(_Meta):
        unique_together = ('account',)

class Artisan(AccountModel):
    slug = models.CharField(choices=var.ARTISAN_CHOICES,max_length=16)
    level = models.IntegerField()
    stepMax = models.IntegerField()
    stepCurrent = models.IntegerField()
    hardcore = models.BooleanField(default=False)
    __unicode__ = lambda self: "%s - %s %s"%(self.slug,self.account,"(hardcore)" if self.hardcore else "")
    class Meta(_Meta):
        unique_together = ('account','slug','hardcore')
