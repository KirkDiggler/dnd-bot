from enum import Enum
from .common import ReferenceItem, ReferenceType
from src.api.lib import proficiencylib

class ProficiencyType(Enum):
    ARMOR = "Armor"
    WEAPON = "Weapons"
    ARTISAN_TOOL = "Artisan's Tools"
    SKILL = "Skills"
    GAMING_SET = "Gaming Sets"
    MUSICAL_INSTRUMENT = "Musical Instruments"
    OTHER = "Other"
    SAVING_THROW = "Saving Throws"
    LANGUAGE = "Language"

class Proficiency:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == 'reference':
                    setattr(self, key, ReferenceItem(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])

    def to_model(self):
        return proficiencylib.Proficiency(
            key=self.index,
            name=self.name,
            type=_proficiency_to_proficiency_type_model(self),
        )

# breaks up weapon type into weapon category and weapon type
def _proficiency_to_proficiency_type_model(input):
    lookup = {
        "Weapons": proficiencylib.ProficiencyType.WEAPON,
        "Armor": proficiencylib.ProficiencyType.ARMOR,
        "Artisan's Tools": proficiencylib.ProficiencyType.TOOL,
        "Skills": proficiencylib.ProficiencyType.SKILL,
        "Saving Throws": proficiencylib.ProficiencyType.SAVING_THROW,
        "Other": proficiencylib.ProficiencyType.OTHER,
    }
    if lookup[input.type] == proficiencylib.ProficiencyType.WEAPON:
        if input.reference.reference_type == ReferenceType.EQUIPMENT_CATEGORY:
            return proficiencylib.ProficiencyType.WEAPON_CATEGORY
        else:
            return proficiencylib.ProficiencyType.WEAPON
    elif lookup[input.type] == proficiencylib.ProficiencyType.ARMOR:
        if input.reference.reference_type == ReferenceType.EQUIPMENT_CATEGORY:
            return proficiencylib.ProficiencyType.ARMOR_CATEGORY
        else:
            return proficiencylib.ProficiencyType.ARMOR
    else:
            return lookup[input.type]

