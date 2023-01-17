class Class:
    def __init__(self, **kwargs):
        allowed_attributes = ['key', 'name', 'hit_die', 'proficiency_choices', 'proficiencies', 'saving_throws', 'starting_equipment', 'starting_equipment_options', 'class_levels']
        __slots__ = '_key', '_name', '_hit_die', '_proficiency_choices', '_proficiencies', '_saving_throws', '_starting_equipment', '_starting_equipment_options', '_class_levels', '_inventory'

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
    def hit_die(self):
        return self._hit_die

    @property
    def proficiency_choices(self):
        return self._proficiency_choices

    @property
    def proficiencies(self):
        return self._proficiencies

    @property
    def saving_throws(self):
        return self._saving_throws

    @property
    def starting_equipment(self):
        return self._starting_equipment

    @property
    def starting_equipment_options(self):
        return self._starting_equipment_options

    @property
    def class_levels(self):
        return self._class_levels

    @property
    def inventory(self):
        return self._inventory