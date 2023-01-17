from enum import Enum
from .equipmentlib import Equipment

class ArmorClass:
    def __init__(self, base: int, dex_bonus: bool):
        self._base = base
        self._dex_bonus = dex_bonus

    @property
    def base(self):
        return self._base

    @property
    def dex_bonus(self):
        return self._dex_bonus
    
class ArmorCategory(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    SHIELD = "shield"

class Armor(Equipment):
    def __init__(self, **kwargs):
        allowed_attributes =  ['str_minimum', 'stealth_disadvantage', 'armor_class', 'armor_category']
        __slots__ = '_str_minimum', '_stealth_disadvantage', '_armor_class', '_armor_category'

        super().__init__(**kwargs)

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def str_minimum(self):
        return self._str_minimum

    @property
    def stealth_disadvantage(self):
        return self._stealth_disadvantage

    @property
    def armor_class(self):
        return self._armor_class

    @property
    def armor_category(self):
        return self._armor_category