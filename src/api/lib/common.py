class Dice:
    def __init__(self, **kwargs):
        allowed_values = ['quantity', 'die']
        __slots__ = '_quantity', '_die'

        for key in kwargs:
            if key in allowed_values:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def quantity(self):
        return self._quantity

    @property
    def die(self):
        return self._die
