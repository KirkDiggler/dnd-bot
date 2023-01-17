from enum import Enum
from .equipmentlib import Equipment
from .cost import Cost

class WeaponCategory(Enum):
    MARTIAL = "martial-weapon"
    MARTIAL_MELEE = "martial-melee"
    MARTIAL_RANGED = "martial-ranged"
    RANGED_WEAPON = "ranged-weapon"
    SIMPLE = "simple-weapon"
    SIMPLE_MELEE = "Simple Melee"
    SIMPLE_RANGED = "Simple Ranged"

class Weapon(Equipment):
    def __init__(self, **kwargs):
        allowed_attributes = ['weapon_category', 'weapon_range', 'category_range', 'damage', 'range']
        __slots__ = '_weapon_category', '_weapon_range', '_category_range', '_damage', '_range'

        self._weapon_range = None
        super().__init__(**kwargs)

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def weapon_category(self):
        return self._weapon_category

    @property
    def weapon_range(self):
        return self._weapon_range

    @property
    def category_range(self):
        return self._category_range

    @property
    def damage_dice(self):
        return self._damage_dice

    @property
    def damage(self):
        return self._damage

    @property
    def range(self):
        return self._range

    @property
    def properties(self):
        return self._properties
