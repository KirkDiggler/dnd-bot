import random
import math
from src.api.dnd5eapi.client import Client
from src.api.lib import proficiencylib, referencelib

class Character:
    def __init__(self, name: str):
        __slots__ = '_client', '_name', '_max_hitpoints', '_hitpoints', '_creation_steps', \
            '_ability_scores', '_ability_bonuses', '_proficiencies', '_proficiency_choices', \
            '_class', '_race', '_background', '_alignment', '_experience_points', \
            '_saving_throws', '_skills', '_spells', '_spell_slots', '_inventory', \
            '_equipment', '_weapons', '_armor', '_tools', '_languages', '_features'

        self._name = name
        self._client = Client()
        self._character_started = False
        self._proficiencies = {
            proficiencylib.ProficiencyType.ARMOR: [],
            proficiencylib.ProficiencyType.ARMOR_CATEGORY: [],
            proficiencylib.ProficiencyType.WEAPON: [],
            proficiencylib.ProficiencyType.WEAPON_CATEGORY: [],
            proficiencylib.ProficiencyType.SKILL: [],
            proficiencylib.ProficiencyType.TOOL: [],
            proficiencylib.ProficiencyType.SAVING_THROW: [],
            proficiencylib.ProficiencyType.LANGUAGE: [],
            proficiencylib.ProficiencyType.OTHER: []
        }
        self._proficiency_choices = []
        self._proficiecies_chosen = False
        self._equipment_choices = []
        self._saving_throws = []
        self._ability_scores = {
            'con': {'roll': 0, 'bonus': 0},
            'str': {'roll': 0, 'bonus': 0},
            'dex': {'roll': 0, 'bonus': 0},
            'int': {'roll': 0, 'bonus': 0},
            'wis': {'roll': 0, 'bonus': 0},
            'cha': {'roll': 0, 'bonus': 0}
        }
        self._ability_bonuses = []

        self._hit_die = 0
        self._hit_points = 0
        self._profiency_bonus = 2
        self._class = None
        self._race = None

        self._creation_steps = {
            'started': False,
            'ability_scores': False,
            'class': False,
            'race': False,
            'background': False,
            'alignment': False,
            'experience_points': False,
            'saving_throws': False,
            'skills': False,
            'spells': False,
            'inventory': False,
            'equipment': False,
            'weapons': False,
            'armor': False,
            'languages': False,
            'features': False,
            'finished': False
        }

    def __str__(self):
        return self._name + ' the ' + self._race.name + ' ' + self._class.name

    @property
    def name(self):
        return self._name

    def get_class(self):
        if self._class is None:
            return 'No class'

        return self._class

    @property
    def hit_die(self):
        return self._hit_die

    @property
    def hit_points(self):
        return self._hit_points

    @property
    def profiency_bonus(self):
        return self._profiency_bonus

    @property
    def proficiencies(self):
        return self._proficiencies
    
    @property
    def starting_equipment_options(self):
        return self._class.starting_equipment_options

    @property
    def proficiency_choices(self):
        return self._proficiency_choices

    # TODO: create a CreateOptions class, can set templates with it
    def create(self, options: dict):
        if self._creation_steps['started']:
            raise Exception("Character already started")
        
        self._creation_steps['started'] = True

        self._class = self._client.get_class(options['class'])
        self._hit_die = self._class.hit_die
        
        proficiencies = [self._client.get_proficiency(p.key) for p in self._class.proficiencies]
        self._add_proficiencies(proficiencies)

        self._race = self._client.get_race(options['race'])
    
        if self._class.proficiency_choices:
            self._proficiency_choices = self._class.proficiency_choices

        if self._race.starting_proficiency_options:
            self._proficiency_choices.append(self._race.starting_proficiency_options)

    def _add_proficiencies(self, proficiencies: list):
        for proficiency in proficiencies:
            # TODO: prevent duplicates
            self._proficiencies[proficiency.type].append(proficiency)

    def _add_inventory(self, reference: referencelib.ReferenceItem):
        equipment = self.client.get_equipment(name=reference.key)
        self._inventory[equipment.category].append(equipment)
