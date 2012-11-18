# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table('diablo_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('diablo', ['Region'])

        # Adding model 'Account'
        db.create_table('diablo_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='diablo_accounts', null=True, to=orm['auth.User'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Region'])),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('lastHeroPlayed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lastUpdated', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('diablo', ['Account'])

        # Adding model 'Kills'
        db.create_table('diablo_kills', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['diablo.Account'], unique=True)),
            ('monsters', self.gf('django.db.models.fields.IntegerField')()),
            ('elites', self.gf('django.db.models.fields.IntegerField')()),
            ('hardcoreMonsters', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('diablo', ['Kills'])

        # Adding unique constraint on 'Kills', fields ['account']
        db.create_unique('diablo_kills', ['account_id'])

        # Adding model 'TimePlayed'
        db.create_table('diablo_timeplayed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['diablo.Account'], unique=True)),
            ('barbarian', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('demonhunter', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('monk', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('witchdoctor', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('wizard', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('diablo', ['TimePlayed'])

        # Adding unique constraint on 'TimePlayed', fields ['account']
        db.create_unique('diablo_timeplayed', ['account_id'])

        # Adding model 'Artisan'
        db.create_table('diablo_artisan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Account'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
            ('stepMax', self.gf('django.db.models.fields.IntegerField')()),
            ('stepCurrent', self.gf('django.db.models.fields.IntegerField')()),
            ('hardcore', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('diablo', ['Artisan'])

        # Adding unique constraint on 'Artisan', fields ['account', 'slug', 'hardcore']
        db.create_unique('diablo_artisan', ['account_id', 'slug', 'hardcore'])

        # Adding model 'Hero'
        db.create_table('diablo_hero', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Account'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.IntegerField')()),
            ('lastUpdated', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('dead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hardcore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('elite_kills', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('diablo', ['Hero'])

        # Adding unique constraint on 'Hero', fields ['account', 'id']
        db.create_unique('diablo_hero', ['account_id', 'id'])

        # Adding M2M table for field items on 'Hero'
        db.create_table('diablo_hero_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hero', models.ForeignKey(orm['diablo.hero'], null=False)),
            ('item', models.ForeignKey(orm['diablo.item'], null=False))
        ))
        db.create_unique('diablo_hero_items', ['hero_id', 'item_id'])

        # Adding model 'Skill'
        db.create_table('diablo_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('simpleDescription', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tooltipUrl', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('diablo', ['Skill'])

        # Adding unique constraint on 'Skill', fields ['slug']
        db.create_unique('diablo_skill', ['slug'])

        # Adding model 'Rune'
        db.create_table('diablo_rune', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('simpleDescription', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Skill'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('tooltipParams', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('diablo', ['Rune'])

        # Adding unique constraint on 'Rune', fields ['slug', 'skill']
        db.create_unique('diablo_rune', ['slug', 'skill_id'])

        # Adding model 'SkillSet'
        db.create_table('diablo_skillset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hero', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['diablo.Hero'], unique=True)),
        ))
        db.send_create_signal('diablo', ['SkillSet'])

        # Adding M2M table for field runes on 'SkillSet'
        db.create_table('diablo_skillset_runes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skillset', models.ForeignKey(orm['diablo.skillset'], null=False)),
            ('rune', models.ForeignKey(orm['diablo.rune'], null=False))
        ))
        db.create_unique('diablo_skillset_runes', ['skillset_id', 'rune_id'])

        # Adding M2M table for field passive_skills on 'SkillSet'
        db.create_table('diablo_skillset_passive_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skillset', models.ForeignKey(orm['diablo.skillset'], null=False)),
            ('skill', models.ForeignKey(orm['diablo.skill'], null=False))
        ))
        db.create_unique('diablo_skillset_passive_skills', ['skillset_id', 'skill_id'])

        # Adding model 'Follower'
        db.create_table('diablo_follower', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hero', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Hero'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('diablo', ['Follower'])

        # Adding unique constraint on 'Follower', fields ['slug', 'hero']
        db.create_unique('diablo_follower', ['slug', 'hero_id'])

        # Adding M2M table for field items on 'Follower'
        db.create_table('diablo_follower_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('follower', models.ForeignKey(orm['diablo.follower'], null=False)),
            ('item', models.ForeignKey(orm['diablo.item'], null=False))
        ))
        db.create_unique('diablo_follower_items', ['follower_id', 'item_id'])

        # Adding M2M table for field skills on 'Follower'
        db.create_table('diablo_follower_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('follower', models.ForeignKey(orm['diablo.follower'], null=False)),
            ('skill', models.ForeignKey(orm['diablo.skill'], null=False))
        ))
        db.create_unique('diablo_follower_skills', ['follower_id', 'skill_id'])

        # Adding model 'Stats'
        db.create_table('diablo_stats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hero', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['diablo.Hero'], unique=True)),
            ('damageIncrease', self.gf('django.db.models.fields.FloatField')()),
            ('damageReduction', self.gf('django.db.models.fields.FloatField')()),
            ('critChance', self.gf('django.db.models.fields.FloatField')()),
            ('life', self.gf('django.db.models.fields.IntegerField')()),
            ('strength', self.gf('django.db.models.fields.IntegerField')()),
            ('dexterity', self.gf('django.db.models.fields.IntegerField')()),
            ('intelligence', self.gf('django.db.models.fields.IntegerField')()),
            ('vitality', self.gf('django.db.models.fields.IntegerField')()),
            ('armor', self.gf('django.db.models.fields.IntegerField')()),
            ('coldResist', self.gf('django.db.models.fields.IntegerField')()),
            ('fireResist', self.gf('django.db.models.fields.IntegerField')()),
            ('lightningResist', self.gf('django.db.models.fields.IntegerField')()),
            ('poisonResist', self.gf('django.db.models.fields.IntegerField')()),
            ('arcaneResist', self.gf('django.db.models.fields.IntegerField')()),
            ('damage', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('diablo', ['Stats'])

        # Adding unique constraint on 'Stats', fields ['hero']
        db.create_unique('diablo_stats', ['hero_id'])

        # Adding model 'Act'
        db.create_table('diablo_act', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('diablo', ['Act'])

        # Adding model 'Quest'
        db.create_table('diablo_quest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('act', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Act'])),
        ))
        db.send_create_signal('diablo', ['Quest'])

        # Adding unique constraint on 'Quest', fields ['act', 'slug']
        db.create_unique('diablo_quest', ['act_id', 'slug'])

        # Adding model 'Progression'
        db.create_table('diablo_progression', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Account'])),
            ('difficulty', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('hardcore', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('diablo', ['Progression'])

        # Adding unique constraint on 'Progression', fields ['account', 'hardcore', 'difficulty']
        db.create_unique('diablo_progression', ['account_id', 'hardcore', 'difficulty'])

        # Adding M2M table for field completed_acts on 'Progression'
        db.create_table('diablo_progression_completed_acts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('progression', models.ForeignKey(orm['diablo.progression'], null=False)),
            ('act', models.ForeignKey(orm['diablo.act'], null=False))
        ))
        db.create_unique('diablo_progression_completed_acts', ['progression_id', 'act_id'])

        # Adding M2M table for field completed_quests on 'Progression'
        db.create_table('diablo_progression_completed_quests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('progression', models.ForeignKey(orm['diablo.progression'], null=False)),
            ('quest', models.ForeignKey(orm['diablo.quest'], null=False))
        ))
        db.create_unique('diablo_progression_completed_quests', ['progression_id', 'quest_id'])

        # Adding model 'Progress'
        db.create_table('diablo_progress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('difficulty', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('hero', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.Hero'])),
        ))
        db.send_create_signal('diablo', ['Progress'])

        # Adding unique constraint on 'Progress', fields ['hero', 'difficulty']
        db.create_unique('diablo_progress', ['hero_id', 'difficulty'])

        # Adding M2M table for field completed_acts on 'Progress'
        db.create_table('diablo_progress_completed_acts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('progress', models.ForeignKey(orm['diablo.progress'], null=False)),
            ('act', models.ForeignKey(orm['diablo.act'], null=False))
        ))
        db.create_unique('diablo_progress_completed_acts', ['progress_id', 'act_id'])

        # Adding M2M table for field completed_quests on 'Progress'
        db.create_table('diablo_progress_completed_quests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('progress', models.ForeignKey(orm['diablo.progress'], null=False)),
            ('quest', models.ForeignKey(orm['diablo.quest'], null=False))
        ))
        db.create_unique('diablo_progress_completed_quests', ['progress_id', 'quest_id'])

        # Adding model 'AttributeType'
        db.create_table('diablo_attributetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string_format', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('classifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('diablo', ['AttributeType'])

        # Adding model 'Attribute'
        db.create_table('diablo_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diablo.AttributeType'])),
        ))
        db.send_create_signal('diablo', ['Attribute'])

        # Adding model 'Item'
        db.create_table('diablo_item', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('displayColor', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tooltipParams', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slot', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('diablo', ['Item'])

        # Adding unique constraint on 'Item', fields ['id', 'slot', 'icon']
        db.create_unique('diablo_item', ['id', 'slot', 'icon'])

        # Adding M2M table for field attributes on 'Item'
        db.create_table('diablo_item_attributes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['diablo.item'], null=False)),
            ('attribute', models.ForeignKey(orm['diablo.attribute'], null=False))
        ))
        db.create_unique('diablo_item_attributes', ['item_id', 'attribute_id'])

        # Adding M2M table for field gems on 'Item'
        db.create_table('diablo_item_gems', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['diablo.item'], null=False)),
            ('gem', models.ForeignKey(orm['diablo.gem'], null=False))
        ))
        db.create_unique('diablo_item_gems', ['item_id', 'gem_id'])

        # Adding model 'Gem'
        db.create_table('diablo_gem', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('displayColor', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tooltipParams', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('diablo', ['Gem'])

        # Adding unique constraint on 'Gem', fields ['id', 'icon']
        db.create_unique('diablo_gem', ['id', 'icon'])

        # Adding M2M table for field attributes on 'Gem'
        db.create_table('diablo_gem_attributes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gem', models.ForeignKey(orm['diablo.gem'], null=False)),
            ('attribute', models.ForeignKey(orm['diablo.attribute'], null=False))
        ))
        db.create_unique('diablo_gem_attributes', ['gem_id', 'attribute_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Gem', fields ['id', 'icon']
        db.delete_unique('diablo_gem', ['id', 'icon'])

        # Removing unique constraint on 'Item', fields ['id', 'slot', 'icon']
        db.delete_unique('diablo_item', ['id', 'slot', 'icon'])

        # Removing unique constraint on 'Progress', fields ['hero', 'difficulty']
        db.delete_unique('diablo_progress', ['hero_id', 'difficulty'])

        # Removing unique constraint on 'Progression', fields ['account', 'hardcore', 'difficulty']
        db.delete_unique('diablo_progression', ['account_id', 'hardcore', 'difficulty'])

        # Removing unique constraint on 'Quest', fields ['act', 'slug']
        db.delete_unique('diablo_quest', ['act_id', 'slug'])

        # Removing unique constraint on 'Stats', fields ['hero']
        db.delete_unique('diablo_stats', ['hero_id'])

        # Removing unique constraint on 'Follower', fields ['slug', 'hero']
        db.delete_unique('diablo_follower', ['slug', 'hero_id'])

        # Removing unique constraint on 'Rune', fields ['slug', 'skill']
        db.delete_unique('diablo_rune', ['slug', 'skill_id'])

        # Removing unique constraint on 'Skill', fields ['slug']
        db.delete_unique('diablo_skill', ['slug'])

        # Removing unique constraint on 'Hero', fields ['account', 'id']
        db.delete_unique('diablo_hero', ['account_id', 'id'])

        # Removing unique constraint on 'Artisan', fields ['account', 'slug', 'hardcore']
        db.delete_unique('diablo_artisan', ['account_id', 'slug', 'hardcore'])

        # Removing unique constraint on 'TimePlayed', fields ['account']
        db.delete_unique('diablo_timeplayed', ['account_id'])

        # Removing unique constraint on 'Kills', fields ['account']
        db.delete_unique('diablo_kills', ['account_id'])

        # Deleting model 'Region'
        db.delete_table('diablo_region')

        # Deleting model 'Account'
        db.delete_table('diablo_account')

        # Deleting model 'Kills'
        db.delete_table('diablo_kills')

        # Deleting model 'TimePlayed'
        db.delete_table('diablo_timeplayed')

        # Deleting model 'Artisan'
        db.delete_table('diablo_artisan')

        # Deleting model 'Hero'
        db.delete_table('diablo_hero')

        # Removing M2M table for field items on 'Hero'
        db.delete_table('diablo_hero_items')

        # Deleting model 'Skill'
        db.delete_table('diablo_skill')

        # Deleting model 'Rune'
        db.delete_table('diablo_rune')

        # Deleting model 'SkillSet'
        db.delete_table('diablo_skillset')

        # Removing M2M table for field runes on 'SkillSet'
        db.delete_table('diablo_skillset_runes')

        # Removing M2M table for field passive_skills on 'SkillSet'
        db.delete_table('diablo_skillset_passive_skills')

        # Deleting model 'Follower'
        db.delete_table('diablo_follower')

        # Removing M2M table for field items on 'Follower'
        db.delete_table('diablo_follower_items')

        # Removing M2M table for field skills on 'Follower'
        db.delete_table('diablo_follower_skills')

        # Deleting model 'Stats'
        db.delete_table('diablo_stats')

        # Deleting model 'Act'
        db.delete_table('diablo_act')

        # Deleting model 'Quest'
        db.delete_table('diablo_quest')

        # Deleting model 'Progression'
        db.delete_table('diablo_progression')

        # Removing M2M table for field completed_acts on 'Progression'
        db.delete_table('diablo_progression_completed_acts')

        # Removing M2M table for field completed_quests on 'Progression'
        db.delete_table('diablo_progression_completed_quests')

        # Deleting model 'Progress'
        db.delete_table('diablo_progress')

        # Removing M2M table for field completed_acts on 'Progress'
        db.delete_table('diablo_progress_completed_acts')

        # Removing M2M table for field completed_quests on 'Progress'
        db.delete_table('diablo_progress_completed_quests')

        # Deleting model 'AttributeType'
        db.delete_table('diablo_attributetype')

        # Deleting model 'Attribute'
        db.delete_table('diablo_attribute')

        # Deleting model 'Item'
        db.delete_table('diablo_item')

        # Removing M2M table for field attributes on 'Item'
        db.delete_table('diablo_item_attributes')

        # Removing M2M table for field gems on 'Item'
        db.delete_table('diablo_item_gems')

        # Deleting model 'Gem'
        db.delete_table('diablo_gem')

        # Removing M2M table for field attributes on 'Gem'
        db.delete_table('diablo_gem_attributes')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'diablo.account': {
            'Meta': {'object_name': 'Account'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastHeroPlayed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lastUpdated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Region']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'diablo_accounts'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'diablo.act': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Act'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'diablo.artisan': {
            'Meta': {'unique_together': "(('account', 'slug', 'hardcore'),)", 'object_name': 'Artisan'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Account']"}),
            'hardcore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'stepCurrent': ('django.db.models.fields.IntegerField', [], {}),
            'stepMax': ('django.db.models.fields.IntegerField', [], {})
        },
        'diablo.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.AttributeType']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'diablo.attributetype': {
            'Meta': {'object_name': 'AttributeType'},
            'classifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'string_format': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'diablo.follower': {
            'Meta': {'ordering': "('-slug',)", 'unique_together': "(('slug', 'hero'),)", 'object_name': 'Follower'},
            'hero': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Hero']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Item']", 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Skill']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'diablo.gem': {
            'Meta': {'unique_together': "(('id', 'icon'),)", 'object_name': 'Gem'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Attribute']", 'null': 'True', 'blank': 'True'}),
            'displayColor': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tooltipParams': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'diablo.hero': {
            'Meta': {'unique_together': "(('account', 'id'),)", 'object_name': 'Hero'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Account']"}),
            'dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'elite_kills': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gender': ('django.db.models.fields.IntegerField', [], {}),
            'hardcore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Item']", 'null': 'True', 'blank': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'lastUpdated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'diablo.item': {
            'Meta': {'unique_together': "(('id', 'slot', 'icon'),)", 'object_name': 'Item'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Attribute']", 'null': 'True', 'blank': 'True'}),
            'displayColor': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gems': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Gem']", 'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'tooltipParams': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'diablo.kills': {
            'Meta': {'unique_together': "(('account',),)", 'object_name': 'Kills'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['diablo.Account']", 'unique': 'True'}),
            'elites': ('django.db.models.fields.IntegerField', [], {}),
            'hardcoreMonsters': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monsters': ('django.db.models.fields.IntegerField', [], {})
        },
        'diablo.progress': {
            'Meta': {'unique_together': "(('hero', 'difficulty'),)", 'object_name': 'Progress'},
            'completed_acts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Act']", 'null': 'True', 'blank': 'True'}),
            'completed_quests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Quest']", 'null': 'True', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'hero': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Hero']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'diablo.progression': {
            'Meta': {'unique_together': "(('account', 'hardcore', 'difficulty'),)", 'object_name': 'Progression'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Account']"}),
            'completed_acts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Act']", 'null': 'True', 'blank': 'True'}),
            'completed_quests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Quest']", 'null': 'True', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'hardcore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'diablo.quest': {
            'Meta': {'ordering': "('act',)", 'unique_together': "(('act', 'slug'),)", 'object_name': 'Quest'},
            'act': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Act']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'})
        },
        'diablo.region': {
            'Meta': {'object_name': 'Region'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'diablo.rune': {
            'Meta': {'unique_together': "(('slug', 'skill'),)", 'object_name': 'Rune'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'simpleDescription': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diablo.Skill']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'tooltipParams': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'diablo.skill': {
            'Meta': {'unique_together': "(('slug',),)", 'object_name': 'Skill'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'simpleDescription': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'tooltipUrl': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'diablo.skillset': {
            'Meta': {'object_name': 'SkillSet'},
            'hero': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['diablo.Hero']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passive_skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Skill']", 'null': 'True', 'blank': 'True'}),
            'runes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['diablo.Rune']", 'null': 'True', 'blank': 'True'})
        },
        'diablo.stats': {
            'Meta': {'unique_together': "(('hero',),)", 'object_name': 'Stats'},
            'arcaneResist': ('django.db.models.fields.IntegerField', [], {}),
            'armor': ('django.db.models.fields.IntegerField', [], {}),
            'coldResist': ('django.db.models.fields.IntegerField', [], {}),
            'critChance': ('django.db.models.fields.FloatField', [], {}),
            'damage': ('django.db.models.fields.FloatField', [], {}),
            'damageIncrease': ('django.db.models.fields.FloatField', [], {}),
            'damageReduction': ('django.db.models.fields.FloatField', [], {}),
            'dexterity': ('django.db.models.fields.IntegerField', [], {}),
            'fireResist': ('django.db.models.fields.IntegerField', [], {}),
            'hero': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['diablo.Hero']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intelligence': ('django.db.models.fields.IntegerField', [], {}),
            'life': ('django.db.models.fields.IntegerField', [], {}),
            'lightningResist': ('django.db.models.fields.IntegerField', [], {}),
            'poisonResist': ('django.db.models.fields.IntegerField', [], {}),
            'strength': ('django.db.models.fields.IntegerField', [], {}),
            'vitality': ('django.db.models.fields.IntegerField', [], {})
        },
        'diablo.timeplayed': {
            'Meta': {'unique_together': "(('account',),)", 'object_name': 'TimePlayed'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['diablo.Account']", 'unique': 'True'}),
            'barbarian': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'demonhunter': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monk': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'witchdoctor': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'wizard': ('django.db.models.fields.FloatField', [], {'default': '0'})
        }
    }

    complete_apps = ['diablo']