from .common import ReferenceItem
from .choice import Choice
from .ability_score import AbilityScore
from src.api.lib import classlib, starting_equipment

class StartingEquipment:
    def __init__(self, *json):
        for dictionary in json:
            for key in dictionary:
                if key == 'equipment':
                    setattr(self, key, ReferenceItem(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])

    def to_model(self):
        return starting_equipment.StartingEquipment(
            equipment=self.equipment.to_model(),
            quantity=self.quantity
        )

class CharacterClass:
    def __init__(self, *json):
        for dictionary in json:
            for key in dictionary:
                if key == 'proficiencies':
                    setattr(self, key, [ReferenceItem(p) for p in dictionary[key]])
                elif key == "saving_throws":
                    setattr(self, key, [AbilityScore(a) for a in dictionary[key]])
                elif key == "starting_equipment":
                    setattr(self, key, [StartingEquipment(s) for s in dictionary[key]])
                else:
                    setattr(self, key, dictionary[key])

    def __str__(self):
        return self.name

    def to_model(self):
        return classlib.Class(
            key=self.index,
            name=self.name,
            hit_die=self.hit_die,
            proficiencies=[p.to_model() for p in self.proficiencies],
            proficiency_choices=[Choice(c).to_model() for c in self.proficiency_choices],
            starting_equipment=[s.to_model() for s in self.starting_equipment],
            starting_equipment_options=[Choice(c).to_model() for c in self.starting_equipment_options],
            saving_throws=[a.to_model() for a in self.saving_throws],
            class_levels=[l.to_model() for l in self.class_levels]
        )