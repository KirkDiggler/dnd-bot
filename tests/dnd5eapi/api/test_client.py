import requests_cache
import requests_mock
from unittest import TestCase

from src.api.dnd5eapi.client import Client
from src.models.reference import ReferenceType
from src.models.choice import OptionType
from src.models.weapon import WeaponCategory
from src.models.equipment import EquipmentCategory
from src.models.proficiency import ProficiencyType
from src.models.cost import CostUnit
class TestClient(TestCase):
    def setUp(self):
        super(TestClient, self).setUp()
        requests_cache.clear()

    def test_get_class(self):
        client = Client()

        class_ = client.get_class(name='monk')

        self.assertEqual(class_.key, "monk")
        self.assertEqual(class_.name, "Monk")
        self.assertEqual(class_.hit_die, 8)
        self.assertEqual(len(class_.proficiencies), 4)
        self.assertEqual(class_.proficiencies[0].name, "Simple Weapons")
        self.assertEqual(len(class_.proficiency_choices), 2)
        self.assertEqual(class_.proficiency_choices[0].choose, 2)
        self.assertEqual(len(class_.proficiency_choices[1].option_list), 2)
        self.assertEqual(class_.proficiency_choices[1].option_list[0].type, OptionType.CHOICE)
        
        second_choice = class_.proficiency_choices[1].option_list[0]
        self.assertEqual(second_choice.choose, 1)
        self.assertEqual(len(second_choice.option_list), 19)
        self.assertEqual(second_choice.option_list[0].type, OptionType.REFERENCE)
        self.assertEqual(second_choice.option_list[0].item.type, ReferenceType.PROFICIENCY)
        self.assertEqual(second_choice.option_list[0].item.key, "alchemists-supplies")
        self.assertEqual(second_choice.option_list[0].item.name, "Alchemist's Supplies")

        self.assertEqual(len(class_.saving_throws), 2)

        self.assertEqual(class_.saving_throws[0].key, "str")
        self.assertEqual(class_.saving_throws[0].name, "STR")
        self.assertEqual(class_.saving_throws[1].key, "dex")
        self.assertEqual(class_.saving_throws[1].name, "DEX")

        self.assertEqual(len(class_.class_levels), 20)
        self.assertEqual(class_.class_levels[0].level, 1)
        self.assertEqual(class_.class_levels[0].ability_score_bonuses, 0)
        self.assertEqual(class_.class_levels[3].ability_score_bonuses, 1)
        self.assertEqual(class_.class_levels[0].proficiency_bonus, 2)
        self.assertEqual(class_.class_levels[4].proficiency_bonus, 3)

        self.assertEqual(len(class_.starting_equipment), 1)
        self.assertEqual(len(class_.starting_equipment_options), 2)

    def test_list_classes(self):
        client = Client()

        classes = client.list_classes()

        self.assertEqual(len(classes), 12)
        self.assertEqual(classes[0].key, "barbarian")
        self.assertEqual(classes[0].name, "Barbarian")
        self.assertEqual(classes[0].type, ReferenceType.CLASS)

    def test_get_equipment(self):
        client = Client()

        equipment = client.get_equipment(name='club')

        self.assertEqual(equipment.key, "club")
        self.assertEqual(equipment.name, "Club")
        self.assertEqual(equipment.category, EquipmentCategory.WEAPON)
        self.assertEqual(equipment.weapon_category, WeaponCategory.SIMPLE)
        self.assertEqual(equipment.weapon_range, "Melee")
        self.assertEqual(equipment.category_range, "Simple Melee")
        self.assertEqual(equipment.cost.quantity, 1)
        self.assertEqual(equipment.cost.unit, CostUnit.SILVER)
        self.assertEqual(equipment.damage.dice_count, 1)
        self.assertEqual(equipment.damage.dice_type, 4)
        self.assertEqual(equipment.damage.type, "bludgeoning")
        self.assertEqual(equipment.weight, 2)
        self.assertEqual(equipment.properties[0].name, "Light")
        self.assertEqual(equipment.properties[0].type, ReferenceType.WEAPON_PROPERTY)
        self.assertEqual(equipment.properties[1].name, "Monk")
        self.assertEqual(equipment.properties[1].type, ReferenceType.WEAPON_PROPERTY)

    def test_list_races(self):
            client = Client()

            races = client.list_races()

            self.assertEqual(len(races), 9)
            self.assertEqual(races[0].key, "dragonborn")
            self.assertEqual(races[0].name, "Dragonborn")
            self.assertEqual(races[0].type, ReferenceType.RACE)

    def test_get_race(self):
        client = Client()

        race = client.get_race(name='dragonborn')

        self.assertEqual(race.key, "dragonborn")
        self.assertEqual(race.name, "Dragonborn")
        self.assertEqual(race.speed, 30)
        self.assertEqual(len(race.ability_bonuses), 2)
        self.assertEqual(race.ability_bonuses[0].ability_score.key, "str")
        self.assertEqual(race.ability_bonuses[0].ability_score.name, "STR")
        self.assertEqual(len(race.languages), 2)
        self.assertEqual(len(race.traits), 3)

    def test_get_trait(self):
        client = Client()

        trait = client.get_trait(name='draconic-ancestry')

        self.assertEqual(trait.key, "draconic-ancestry")
        self.assertEqual(trait.name, "Draconic Ancestry")

    def test_get_proficiency(self):
        client = Client()

        proficiency = client.get_proficiency(name='light-armor')

        self.assertEqual(proficiency.key, "light-armor")
        self.assertEqual(proficiency.name, "Light Armor")
        self.assertEqual(proficiency.type, ProficiencyType.ARMOR_CATEGORY)

    def test_list_spells(self):
        client = Client()

        spells = client.list_spells()

        self.assertEqual(len(spells), 319)
        self.assertEqual(spells[0].key, "acid-arrow")
        self.assertEqual(spells[0].name, "Acid Arrow")
        self.assertEqual(spells[0].type, ReferenceType.SPELL)

        level_one_spells = client.list_spells(level='1')

        self.assertEqual(len(level_one_spells), 49)
        self.assertEqual(level_one_spells[0].key, "alarm")
        self.assertEqual(level_one_spells[0].name, "Alarm")

        wizard_spells = client.list_spells(char_class='wizard', level=2)

        self.assertEqual(len(wizard_spells), 31)
        self.assertEqual(wizard_spells[0].key, "acid-arrow")
        self.assertEqual(wizard_spells[0].name, "Acid Arrow")

    def test_get_spell(self):
        client = Client()

        spell = client.get_spell(name='acid-arrow')

        self.assertEqual(spell.key, "acid-arrow")
        self.assertEqual(spell.name, "Acid Arrow")
        self.assertEqual(spell.level, 2)
        self.assertEqual(spell.ritual, False)
        self.assertEqual(spell.casting_time, "1 action")
        self.assertEqual(spell.range, "90 feet")
        self.assertEqual(spell.material, "Powdered rhubarb leaf and an adder's stomach.")
        self.assertEqual(spell.duration, "Instantaneous")
        self.assertEqual(spell.concentration, False)
        self.assertEqual(spell.higher_level[0], "When you cast this spell using a spell slot of 3rd level or higher, the damage (both initial and later) increases by 1d4 for each slot level above 2nd.")
        self.assertEqual("acid", spell.damage.type)
        self.assertEqual("4d4", spell.damage.damage_at_slot_level['2'])

    def test_class_levels_with_spellcasting(self):
        client = Client()

        class_ = client.get_class(name='wizard')

        self.assertEqual(len(class_.class_levels), 20)
        self.assertEqual(class_.class_levels[0].level, 1)
        self.assertEqual(class_.class_levels[0].spellcasting, True)
        self.assertEqual(class_.class_levels[0].spell_slots.level_1, 2)
        self.assertEqual(class_.class_levels[0].spell_slots.level_2, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.level_3, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.level_4, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.level_5, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.level_6, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.level_7, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.level_8, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.level_9, 0)
        self.assertEqual(class_.class_levels[0].spell_slots.cantrips, 3)
        