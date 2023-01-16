from enum import Enum

class CostUnit(Enum):
    COPPER = "cp"
    SILVER = "sp"
    ELECTRUM = "ep"
    GOLD = "gp"
    PLATINUM = "pp"

class Cost:
    def __init__(self, **kwargs):
        allowed_values = ['quantity', 'unit']
        __slots__ = '_quantity', '_unit'

        for key in kwargs:
            if key in allowed_values:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def quantity(self):
        return self._quantity

    @property
    def unit(self):
        return self._unit
