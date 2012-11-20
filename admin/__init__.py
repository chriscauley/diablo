from django.contrib import admin

from diablo.models import *

class HeroAdmin(admin.ModelAdmin):
    readonly_fields = ('_skills','_passive_skills','_items')
    _items = lambda self,obj: ', '.join([i.admin_link for i in obj.itemset.items.all()])
    _items.allow_tags = True
    _skills = lambda self,obj: ', '.join([rune.admin_link for rune in obj.skillset.runes.all()])
    _skills.allow_tags = True
    _passive_skills = lambda self,obj: ', '.join([s.admin_link for s in obj.skillset.passive_skills.all()])
    _passive_skills.allow_tags = True

class FollowerAdmin(admin.ModelAdmin):
    readonly_fields = ('skills','items')

class AccountAdmin(admin.ModelAdmin):
    inlines = []

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('attributes','gems')

class ToolTipAdmin(admin.ModelAdmin):
    list_filter = ("model",)

admin.site.register(Region)
admin.site.register(Account,AccountAdmin)
admin.site.register(Hero,HeroAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(Skill)
admin.site.register(SkillSet)
admin.site.register(Rune)
admin.site.register(Artisan)
admin.site.register(AttributeType)
admin.site.register(Follower,FollowerAdmin)
admin.site.register(ToolTip,ToolTipAdmin)
