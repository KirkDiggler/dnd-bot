from enum import Enum

class ReferenceType(Enum):
    CLASS = "class"
    EQUIPMENT_CATEGORY = "equipment-category"
    EQUIPMENT = "equipment"
    FEATURE = "feature"
    PROFICIENCY = "proficiency"
    RACE = "race"
    TRAIT = "trait"
    LANGUAGE = "language"
    WEAPON_PROPERTY = "weapon-property"
    SKILL = "skill"
    SUBCLASS = "subclass"
    SUBRACE = "subrace"
    SPELL = "spell"
    MAGIC_ITEM = "magic-item"
    MONSTER = "monster"
    ABILITY_SCORE = "ability-score"
    CONDITION = "condition"
    DAMAGE_TYPE = "damage-type"

# ReferenceItem is a class that represents a reference to another object.
# By checking the type returned you can know what type of object you are
# dealing with.
class ReferenceItem:
    def __init__(self, **kwargs):
        allowed_attributes = ['key', 'name', 'type']
        __slots__ = '_key', '_name', '_type'

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type
