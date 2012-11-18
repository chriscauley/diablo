from django.db import models

from .account import Account, AccountModel
from .abstract import ModelManager, _Meta, Model
from .hero import Hero
from diablo import var

class Act(Model):
    name = models.CharField(max_length=10)
    __unicode__ = lambda self: self.name
    class Meta(_Meta):
        ordering = ("name",)

class Quest(Model):
    slug = models.SlugField(max_length=128)
    name = models.CharField(max_length=128)
    act = models.ForeignKey(Act)
    __unicode__ = lambda self: self.name
    class Meta(_Meta):
        ordering = ("act",)
        unique_together = ('act','slug')

class ProgressModel(Model):
    difficulty = models.CharField(choices=var.DIFFICULTY_CHOICES,max_length=16)
    completed_acts = models.ManyToManyField(Act,null=True,blank=True)
    completed_quests = models.ManyToManyField(Quest,null=True,blank=True)
    @classmethod
    def from_json(clss,uniques={},json={}):
        prog, new = clss.objects.get_or_create(**uniques)
        completed_acts = []
        completed_quests = []
        for a_name, act_json in json.items():
            act, new = Act.objects.get_or_create(name=a_name)
            if act_json['completed']:
                completed_acts.append(act)
            for q_json in act_json['completedQuests']:
                quest, new = Quest.objects.get_or_create(act=act,**q_json)
                completed_quests.append(quest)
        prog.completed_acts = completed_acts
        prog.completed_quests = completed_quests
        prog.save()
        return prog
    class Meta(_Meta):
        abstract = True

class Progression(ProgressModel,AccountModel):
    hardcore = models.BooleanField(default=False)
    class Meta(_Meta):
        unique_together = ('account','hardcore','difficulty')

class Progress(ProgressModel):
    hero = models.ForeignKey(Hero)
    class Meta(_Meta):
        unique_together = ('hero','difficulty')
