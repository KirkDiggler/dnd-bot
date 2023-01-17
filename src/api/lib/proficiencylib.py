from enum import Enum

class ProficiencyType(Enum):
    ARMOR = "armor"
    ARMOR_CATEGORY = "armor-category"
    WEAPON = "weapon"
    WEAPON_CATEGORY = "weapon-category"
    TOOL = "tool"
    SKILL = "skill"
    LANGUAGE = "language"
    SAVING_THROW = "saving-throw"
    OTHER = "other"

    def __str__(self):
        return self.value
        
class Proficiency:
    def __init__(self, **kwargs):
        allowed_attributes = ['key', 'name', 'type', 'desc']
        __slots__ = '_key', '_name', '_type', '_desc'

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    def __str__(self):
        return f"{self.name} ({self.type})"
        
    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def desc(self):
        return self._desc