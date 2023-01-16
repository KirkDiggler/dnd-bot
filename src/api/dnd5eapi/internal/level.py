from .feature import Feature
from .common import ReferenceItem
from src.api.lib import level, spell
class Level:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "features":
                    setattr(self, key, [ReferenceItem(f) for f in dictionary[key]])
                elif key == "class":
                    setattr(self, key, ReferenceItem(dictionary[key]))
                elif key == "spellcasting":
                    setattr(self, key, SpellSlots(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])

    def to_model(self):
        spellcasting = False
        spell_slots = None
        if hasattr(self, "spellcasting"):
            spell_slots = self.spellcasting.to_model()
            spellcasting  = True

        return level.Level(
            level=self.level,
            ability_score_bonuses=self.ability_score_bonuses,
            proficiency_bonus=self.prof_bonus,
            spellcasting=spellcasting,
            spell_slots=spell_slots,
            features=[feature.to_model() for feature in self.features]
        )

class SpellSlots:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def to_model(self):
        return spell.SpellSlot(
            cantrips=self.cantrips_known,
            level_1=self.spell_slots_level_1,
            level_2=self.spell_slots_level_2,
            level_3=self.spell_slots_level_3,
            level_4=self.spell_slots_level_4,
            level_5=self.spell_slots_level_5,
            level_6=self.spell_slots_level_6,
            level_7=self.spell_slots_level_7,
            level_8=self.spell_slots_level_8,
            level_9=self.spell_slots_level_9
        )
