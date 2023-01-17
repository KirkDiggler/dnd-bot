class Race:
    def __init__(self, **kwargs):
        allowed_attributes = ['key', 'name', 'speed', 'ability_bonuses', 'ability_bonus_options', 'alignment', 'age', 'size', 'size_description', 'starting_proficiencies', 'starting_proficiency_options', 'languages', 'language_desc', 'traits', 'subraces']
        __slots__ = '_key', '_name', '_speed', '_ability_bonuses', '_ability_bonus_options', '_alignment', '_age', '_size', '_size_description', '_starting_proficiencies', '_starting_proficiency_options', '_languages', '_language_desc', '_traits', '_subraces'

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
    def speed(self):
        return self._speed

    @property
    def ability_bonuses(self):
        return self._ability_bonuses

    @property
    def ability_bonus_options(self):
        return self._ability_bonus_options

    @property
    def alignment(self):
        return self._alignment

    @property
    def age(self):
        return self._age

    @property
    def size(self):
        return self._size

    @property
    def size_description(self):
        return self._size_description

    @property
    def starting_proficiencies(self):
        return self._starting_proficiencies

    @property
    def starting_proficiency_options(self):
        return self._starting_proficiency_options

    @property
    def languages(self):
        return self._languages

    @property
    def language_desc(self):
        return self._language_desc

    @property
    def traits(self):
        return self._traits

    @property
    def subraces(self):
        return self._subraces

