class StartingEquipment:
    def __init__(self, **kwargs):
        allowed_attributes = ['equipment', 'quantity']
        __slots__ = '_equipment', '_quantity'
        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def equipment(self):
        return self._equipment

    @property
    def quantity(self):
        return self._quantity
