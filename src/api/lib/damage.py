from enum import Enum

class DamageType(Enum):
    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"

class Damage:
    def __init__(self, **kwargs):
        allowed_values = ['type', 'dice_count', 'dice_type']
        __slots__ = '_type', '_dice_count', '_dice_type'

        for key in kwargs:
            if key in allowed_values:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def type(self):
        return self._type

    @property
    def dice_count(self):
        return self._dice_count

    @property
    def dice_type(self):
        return self._dice_type
