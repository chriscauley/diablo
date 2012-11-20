from django.db import models

from .abstract import _Meta, APIModel, Model
from .hero import Skill, Rune
from diablo import var

import re, requests

class AttributeType(models.Model):
    string_format = models.CharField(null=True,blank=True,max_length=128)
    __unicode__ = lambda self: self.string_format
    def save(self,*args,**kwargs):
        if not self.string_format:
            self.string_format = self.string_format
        super(AttributeType,self).save(*args,**kwargs)
    class Meta(_Meta):
        pass

class AttributeManager(models.Manager):
    def get_or_create(self,string=None,*args,**kwargs):
        if not string:
            return super(AttributeManager,self).get_or_create(**kwargs)
        string = string.replace(u'\u2013','-')
        matches = re.findall("\d+",string)
        if matches:
            value = sum([float(i) for i in matches])/len(matches)
        else:
            value = 0
        string_format = re.sub("\d+","#",string).replace("#-#",'#')
        attribute_type,new = AttributeType.objects.get_or_create(string_format = string_format)
        if new:
            pass #print "AttributeType created: %s"%attribute_type
        kwargs.update({'value':value,'type':attribute_type,'text':string})
        return super(AttributeManager,self).get_or_create(**kwargs)

class Attribute(models.Model):
    text = models.CharField(max_length=128)
    value = models.IntegerField()
    type = models.ForeignKey(AttributeType)
    objects = AttributeManager()
    __unicode__ = lambda self: self.text
    class Meta(_Meta):
        pass

class ItemModel(APIModel):
    id = models.CharField(max_length=64)
    _id = models.AutoField(primary_key=True)
    # because tooltip params is unique for hero, item is unique for hero
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=64)
    displayColor = models.CharField(max_length=20)
    tooltipParams = models.TextField(null=True,blank=True)
    attributes = models.ManyToManyField(Attribute,null=True,blank=True)

    __unicode__ = lambda self: self.name
    icon_url = property(lambda self: "http://media.blizzard.com/d3/icons/items/large/%s.png"%self.icon)
    background_url = property(lambda self: "http://us.battle.net/d3/static/images/item/icon-bgs/%s.png"%self.displayColor)
    tooltip_url = property(lambda self: "http://us.battle.net/d3/en/tooltip/%s"%self.tooltipParams)
    api_url = property(lambda self: 'http://us.battle.net/api/d3/data/%s'%(self.tooltipParams))

    class Meta:
        abstract = True

class Item(ItemModel):
    slot = models.CharField(choices=var.SLOT_CHOICES,max_length=32)
    gems = models.ManyToManyField("diablo.Gem",null=True,blank=True)
    updates = ['basics']

    def update_basics(self):
        attributes = []
        for s in self.toon['attributes']:
            attribute, new = Attribute.objects.get_or_create(string=s)
            attributes.append(attribute)
        self.attributes = attributes
        self.save()
    def create_gems(self):
        gems = []
        for g in self.toon.get('gems',[]):
            g.update(g.pop("item"))
            a_set = g.pop('attributes')
            gem = Gem.objects.lazy_from_kwargs(**g)
            attributes = []
            for s in a_set:
                attribute, new = Attribute.objects.get_or_create(string=s)
                attributes.append(attribute)
            gem.attributes = attributes
            gem.save()
            gems.append(gem)
        self.gems = gems
    full_attributes = lambda self: Attribute.objects.filter(models.Q(item=self)|models.Q(gem__item=self))
        
    class Meta(_Meta):
        unique_together = ("id","slot","icon")

class Gem(ItemModel):
    updates = []
    icon_url = lambda self: "http://media.blizzard.com/d3/icons/items/small/%s.png"%self.icon
    class Meta(_Meta):
        unique_together = ("id","icon")

class ToolTipManager(models.Manager):
    def get_rune_html(self,model_pk=None):
        """b.net has no rune tooltip link, so I have to render from template"""
        try:
            return self.get(model='rune',model_pk=model_pk).html
        except self.model.DoesNotExist:
            pass
        from django.shortcuts import render_to_response
        values = {
            'rune': Rune.objects.get(pk=model_pk),
            }
        html = render_to_response('diablo/widgets/rune_tooltip.html',values).content
        tooltip = self.model(model='rune',model_pk=model_pk,html=html)
        tooltip.save()
        return html

    def get_lazy_html(self,*args,**kwargs):
        try:
            return self.get(*args,**kwargs).html
        except self.model.DoesNotExist:
            pass
        tooltip = self.model(**kwargs)
        models = {
            'item': Item,
            'skill': Skill,
            }
        try:
            obj = models[tooltip.model].objects.get(pk=tooltip.model_pk)
        except model.DoesNotExist:
            return "An error has occurred."
        print obj.tooltip_url
        r = requests.get(obj.tooltip_url)
        try:
            r.raise_for_status()
        except:
            return "An error has occurred."
        tooltip.html = r.text
        tooltip.save()
        return tooltip.html

MODEL_CHOICES = (
    ('skill','Skill'),
    ('rune','Rune'),
    ('item','Item'),
    )

class ToolTip(models.Model):
    model = models.CharField(max_length=16,choices=MODEL_CHOICES)
    model_pk = models.IntegerField()
    html = models.TextField(null=True,blank=True)
    objects = ToolTipManager()
    __unicode__ = lambda self: "%s #%s ToolTip"%(self.model.title(),self.model_pk)

    class Meta(_Meta):
        unique_together = ('model','model_pk')
