from enum import Enum
from .common import ReferenceItem

class WeaponCategory(Enum):
    SIMPLE = "Simple"
    MARTIAL = "Martial"

class Range:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

class Damage:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "damage_type":
                    setattr(self, key, ReferenceItem(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])
