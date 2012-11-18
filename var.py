KLASS_CHOICES = (
    ('barbarian','Barbarian'),
    ('witch-doctor','Witch Doctor'),
    ('demon-hunter','Demon Hunter'),
    ('wizard','Wizard'),
    ('monk','Monk'),
    )

KLASS_PRIMARIES = {
    'barbarian': '+# Strength',
    'witch-doctor': '+# Intelligence',
    'demon-hunter': '+# Dexterity',
    'wizard': '+# Intelligence',
    'monk': '+# Dexterity',
  }

KLASS_RESOURCES = {
    'barbarian': {'name': "Fury", 'slug': 'fury', 'primary': 100, 'secondary': '' },
    'witch-doctor': {'name': "Mana", 'slug': 'mana', 'primary': 100, 'secondary': '' },
    'demon-hunter': {'name': "Hatred/ Discipline", 'slug': 'hatred-discipline', 'primary': 100, 'secondary': '' },
    'wizard': {'name': "Arcane Power", 'slug': 'arcane-power', 'primary': 100, 'secondary': '' },
    'monk': {'name': "Spirit", 'slug': 'spirit', 'primary': 150, 'secondary': '' },
}

ARTISAN_CHOICES = (
    ('blacksmith','Blacksmith'),
    ('jeweler','Jeweler'),
    )

DIFFICULTY_CHOICES = (
    ('normal', 'Normal'),
    ('nightmare', "Nightmar"),
    ('hell', 'Hell'),
    ('inferno', 'Inferno'),
    )

GENDER_CHOICES = (
    (0,'Male'),
    (1,'Female'),
    )

TYPE_CHOICES = (
    ('a','a'),
    ('b','b'),
    ('c','c'),
    ('d','d'),
    ('e','e'),
    )

SLOT_CHOICES = (
    ('head','Head'),
    ('torso','Torso'),
    ('feet','Feet'),
    ('hands','Hands'),
    ('shoulders','Shoulders'),
    ('legs','Legs'),
    ('bracers','Bracers'),
    ('mainHand','Main Hand'),
    ('offHand','Off Hand'),
    ('waist','Waist'),
    ('rightFinder','Right Finder'),
    ('leftFinder','Left Finder'),
    ('neck','Neck'),
    ('special','Special'),
    )


FOLLOWER_CHOICES = (
    ('templar','Templar'),
    ('scoundrel','Scoundrel'),
    ('enchantress','Enchantress'),
    )


    
