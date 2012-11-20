# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ToolTip'
        db.create_table('diablo_tooltip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('model_pk', self.gf('django.db.models.fields.IntegerField')()),
            ('html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('diablo', ['ToolTip'])

        # Adding unique constraint on 'ToolTip', fields ['model', 'model_pk']
        db.create_unique('diablo_tooltip', ['model', 'model_pk'])


    def backwards(self, orm):
        # Removing unique constraint on 'ToolTip', fields ['model', 'model_pk']
        db.delete_unique('diablo_tooltip', ['model', 'model_pk'])

        # Deleting model 'ToolTip'
        db.delete_table('diablo_tooltip')


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
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
        },
        'diablo.tooltip': {
            'Meta': {'unique_together': "(('model', 'model_pk'),)", 'object_name': 'ToolTip'},
            'html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'model_pk': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['diablo']