class Language:
    def __init__(self, **kwargs):
        allowed_attributes = ['key', 'name', 'type', 'typical_speakers', 'script']
        __slots__ = '_key', '_name', '_type', '_typical_speakers', '_script'
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
    def type(self):
        return self._type

    @property
    def typical_speakers(self):
        return self._typical_speakers

    @property
    def script(self):
        return self._script

    
    def __str__(self):
        return self.name
