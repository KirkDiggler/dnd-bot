from unittest import TestCase
from src.lib.character import Character
from src.api.lib import proficiencylib

class TestCharacter(TestCase):
    def test_create(self):
        character = Character("Test Character")
        character.create(
            {
                "class": "fighter",
                "race": "dwarf",
            }
        )
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.hit_die, 8)
        self.assertEqual(character.hit_points, 0)
        self.assertEqual(character.profiency_bonus, 2)

        self.assertEqual(len(character.proficiencies[proficiencylib.ProficiencyType.WEAPON_CATEGORY]), 1)
        self.assertEqual(character.proficiencies[proficiencylib.ProficiencyType.WEAPON_CATEGORY][0].name, 'Simple Weapons')
        
        self.assertEqual(len(character.proficiencies[proficiencylib.ProficiencyType.WEAPON]), 1)
        self.assertEqual(character.proficiencies[proficiencylib.ProficiencyType.WEAPON][0].name, 'Shortswords')
        

        self.assertEqual(len(character.starting_equipment_options), 2)
        self.assertEqual(character.starting_equipment_options[0].choose, 1)
        self.assertEqual(len(character.starting_equipment_options[0].option_list), 2)
        self.assertEqual(character.starting_equipment_options[0].option_list[0].item.key, 'shortsword')
        self.assertEqual(len(character.starting_equipment_options[0].option_list[1].option_list), 14)
        self.assertEqual(character.starting_equipment_options[0].option_list[1].choose, 1)

        # Choose from the second option that loads all simple weapons
        equip_choice1 = character.starting_equipment_options[0].select('sickle')

        self.assertEqual(equip_choice1.name, 'Sickle')
