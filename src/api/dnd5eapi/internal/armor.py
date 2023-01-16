from enum import Enum

class ArmorCategory(Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    SHIELD = "Shield"


class ArmorClass:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
