from src.api.lib import spell

class Spell:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def to_model(self):
        return spell.Spell(
            key=self.index,
            name=self.name,
            description=self.desc,
            higher_level=self.higher_level,
            range=self.range,
            components=self.components,
            material=self.material,
            ritual=self.ritual,
            duration=self.duration,
            concentration=self.concentration,
            casting_time=self.casting_time,
            level=self.level,
            attack_type=self.attack_type,
            damage=spell.SpellDamage(
                type=self.damage['damage_type']['index'],
                damage_at_slot_level=self.damage['damage_at_slot_level']
            ),
            school=self.school,
        )
