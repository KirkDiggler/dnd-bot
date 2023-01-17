from enum import Enum

class EquipmentCategory(Enum):
    ADVENTURING_GEAR = "adventuring-gear"
    AMMUNITION = "ammunition"
    ARCANE_FOCI = "arcane-foci"
    ARMOR = "armor"
    ARTISAN_TOOL = "artisans-tool"
    DRUIDIC_FOCI = "druidic-foci"
    EQUIPMENT_PACK = "equipment-pack"
    GAMING_SET = "gaming-set"
    HOLY_SYMBOLS = "holy-symbol"
    KITS = "kit" 
    LAND_VEHICLE = "land-vehicle"
    MOUNT = "mount"
    MUSICAL_INSTRUMENT = "musical-instrument"
    POTION = "potion"
    RING = "ring"
    ROD = "rod"
    SCROLL = "scroll"
    STAFF = "staff"
    TOOL = "tools"
    STANDARD_GEAR = "standard-gear"
    WAND = "wand"
    WEAPON = "weapon"

class Equipment:
    def __init__(self, **kwargs):
        allowed_attributes = ['key', 'name', 'category', 'cost', 'weight', 'desc', 'contents', 'properties']
        __slots__ = '_key', '_name', '_category', '_cost', '_weight', '_desc', '_contents', '_properties'

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
    def category(self):
        return self._category

    @property
    def cost(self):
        return self._cost

    @property
    def weight(self):
        return self._weight

    @property
    def desc(self):
        return self._desc

    @property
    def contents(self):
        return self._contents

    @property
    def properties(self):
        return self._properties
