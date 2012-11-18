from django.db import models

from .account import Account
from .abstract import _Meta, APIModel, Model
from diablo import var

class Hero(APIModel):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=64)
    klass = models.CharField(max_length=32,choices=var.KLASS_CHOICES)
    level = models.IntegerField(default=0)
    gender = models.IntegerField(choices=var.GENDER_CHOICES)
    lastUpdated = models.IntegerField(default=0)
    dead = models.BooleanField(default=False)
    hardcore = models.BooleanField(default=False)

    elite_kills = models.IntegerField(default=0)
    items = models.ManyToManyField("diablo.Item",null=True,blank=True)

    __unicode__ = lambda self: "%s by %s"%(self.name,self.account)
    api_url = property(lambda self: '%s/hero/%s'%(self.account.api_url,self.id))
    updates = ['skills','items','followers','stats','progress']

    hardcore_display = lambda self: "hardcore" if self.hardcore else "normal"

    @property
    def progress_left(self):
        from .progress import Act
        count = Act.objects.filter(progress__hero=self).count()
        return count * 42

    def save(self,*args,**kwargs):
        self.klass = getattr(self,'class',self.klass) # taking care of klass vs class problem
        return super(Hero,self).save(*args,**kwargs)

    def update_skills(self):
        runes = []
        passives = []
        for d in self.toon['skills']['active']:
            if not d:
                continue
            s = d['skill']
            s['active'] = True
            skill = Skill.objects.lazy_from_kwargs(**s)
            r = d.pop('rune',{'slug': ''})
            rune = Rune.objects.lazy_from_kwargs(skill=skill,**r)
            runes.append(rune)
        for d in self.toon['skills']['passive']:
            if not d:
                continue
            s = d['skill']
            s['active'] = False
            skill = Skill.objects.lazy_from_kwargs(**s)
            passives.append(skill)
        skillset, new = SkillSet.objects.get_or_create(hero=self)
        skillset.runes = runes
        skillset.passive_skills = passives
        skillset.save()
    def update_items(self):
        from .item import Item
        items = []
        for s,kwargs in self.toon['items'].items():
            item = Item.objects.lazy_from_kwargs(slot=s,**kwargs)
            item.create_gems()
            items.append(item)
        self.items = items
        self.save()
    def update_followers(self):
        from .item import Item
        for slug, json in self.toon['followers'].items():
            items = json.pop('items')
            skills = json.pop('skills')
            follower = Follower.objects.lazy_from_kwargs(hero=self,**json)
            follower.items = [Item.objects.lazy_from_kwargs(slot=s,**j) for s,j in items.items()]
            follower.skills = [Skill.objects.lazy_from_kwargs(**j['skill']) for j in skills if 'skill' in j]
            print follower.skills.all()
            follower.save()
    def update_stats(self):
        json = self.toon['stats']
        stats = Stats.objects.lazy_from_kwargs(hero=self,**json)
    def update_progress(self):
        from .progress import Progress
        for diff, act_json in self.toon['progress'].items():
            uniques = {
                'difficulty':diff,
                'hero': self,
                }
            Progress.from_json(uniques=uniques,json=act_json)
    def gear_bonuses(self):
        from .item import Attribute
        # get all attributes an gem attributes
        totals = Attribute.objects.filter(models.Q(item__hero=self)|models.Q(gem__item__hero=self))
        # We'll need format for printing, type for selecting and primary elevate/ignore
        totals = totals.values('type__string_format','type','type__primary')
        #finally grab everything
        totals = [t for t in totals.annotate(models.Sum('value')) if t['value__sum']]

        #this is really hacky, I hardcoded these from the database
        primary_type = var.KLASS_PRIMARIES[self.klass]
        
        primary_total = [t for t in totals if t['type__primary'] and t['type'] == primary_type]
        secondary_totals = [t for t in totals if not t['type__primary']]
        totals = primary_total + secondary_totals
        for t in totals:
            if "+" in t['type__string_format']:
                t['type__string_format'] = t['type__string_format'].replace("+","")
                t['value__sum'] = "+%s"%t['value__sum']
            t['html'] = t['type__string_format'].replace('#','<span class="value">%s</span>'%t['value__sum'])
        return totals

    def get_resources(self):
        resources = var.KLASS_RESOURCES[self.klass]
        resources['html'] = str(resources['primary'])
        if resources['secondary']:
            resources['html'] += "<br />%s"%resources['secondary']
        return resources

    def display_vitality(self):
        v = self.stats.life
        thousands = v/1000
        if not thousands:
            return v
        hundreds = (v%1000)/100
        return "%s.%sk"%(thousands,hundreds) if hundreds else "%sk"%thousands
    class Meta(_Meta):
        unique_together = ('account','id')

class SkillModel(Model):
    slug = models.SlugField(max_length=64,null=True,blank=True)
    name = models.CharField(max_length=64,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    simpleDescription = models.TextField(null=True,blank=True)
    __unicode__ = lambda self: self.name or '(None)'
    class Meta:
        abstract = True

class Skill(SkillModel):
    icon = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    tooltipUrl = models.CharField(max_length=64,null=True,blank=True)
    tooltip_url = lambda self: "http://us.battle.net/d3/en/%s"%self.tooltipUrl
    icon_url = lambda self: "http://media.blizzard.com/d3/icons/skills/42/%s.png"%self.icon
    class Meta(_Meta):
        unique_together = ('slug',)

class Rune(SkillModel):
    skill = models.ForeignKey(Skill)
    type = models.CharField(max_length=2,choices=var.TYPE_CHOICES,null=True,blank=True)
    tooltipParams = models.TextField(null=True,blank=True)
    tooltip_url = lambda self: "http://us.battle.net/d3/en/%s"%self.tooltipParams
    class Meta(_Meta):
        unique_together = ('slug','skill')

class SkillSet(Model):
    __unicode__ = lambda self: "SkillSet of %s"%self.hero
    hero = models.OneToOneField(Hero)
    runes = models.ManyToManyField(Rune,null=True,blank=True)
    passive_skills = models.ManyToManyField(Skill,null=True,blank=True)
    class Meta(_Meta):
        pass

class Follower(Model):
    hero = models.ForeignKey(Hero)
    __unicode__ = lambda self: "%s Follower - %s"%(self.slug.title(),self.hero)
    slug = models.CharField(choices=var.FOLLOWER_CHOICES,max_length=16)
    level = models.IntegerField()
    items = models.ManyToManyField("diablo.Item",null=True,blank=True)
    skills = models.ManyToManyField(Skill,null=True,blank=True)
    class Meta(_Meta):
        unique_together = ('slug','hero')
        ordering = ('-slug',)

class Stats(Model):
    hero = models.OneToOneField(Hero)
    __unicode__ = lambda self: "Stats - %s"%self.hero
    damageIncrease = models.FloatField()
    damageReduction = models.FloatField()
    critChance = models.FloatField()
    life = models.IntegerField()
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    intelligence = models.IntegerField()
    vitality = models.IntegerField()
    armor = models.IntegerField()
    coldResist = models.IntegerField()
    fireResist = models.IntegerField()
    lightningResist = models.IntegerField()
    poisonResist = models.IntegerField()
    arcaneResist = models.IntegerField()
    damage = models.FloatField()

    _attributes= ['strength','dexterity','intelligence','vitality','armor','damage']
    def attributes(self):
        return [(s,getattr(self,s)) for s in self._attributes]
    class Meta(_Meta):
        unique_together = ('hero',)
