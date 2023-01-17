class SpellSlot:
    def __init__(self, **kwargs):
        self._spells = []
        allowed_attributes = [
            'cantrips', 
            'level_1', 
            'level_2', 
            'level_3', 
            'level_4', 
            'level_5', 
            'level_6', 
            'level_7', 
            'level_8', 
            'level_9']
        __slots__ = '_cantrips', '_level_1', '_level_2', '_level_3', '_level_4', '_level_5', '_level_6', '_level_7', '_level_8', '_level_9', '_spells'

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def cantrips(self):
        return self._cantrips

    @property
    def level_1(self):
        return self._level_1

    @property
    def level_2(self):
        return self._level_2

    @property
    def level_3(self):
        return self._level_3

    @property
    def level_4(self):
        return self._level_4

    @property
    def level_5(self):
        return self._level_5

    @property
    def level_6(self):
        return self._level_6

    @property
    def level_7(self):
        return self._level_7

    @property
    def level_8(self):
        return self._level_8

    @property
    def level_9(self):
        return self._level_9

class Spell:
    def __init__(self, **kwargs):
        allowed_attributes = ['key', 'name', 'attack_type', 'level', 'school', 'casting_time', 'material', 'ritual', 'concentration', 'duration', 'range', 'components', 'damage', 'duration', 'higher_level', 'description']
        __slots__ = '_key', '_name', '_attack_type', '_level', '_school', '_casting_time', '_material', '_ritual', '_concentration', '_duration', '_range', '_components', '_damage', '_duration', '_higher_level', '_description'

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
    def attack_type(self):
        return self._attack_type

    @property
    def level(self):
        return self._level

    @property
    def school(self):
        return self._school

    @property
    def casting_time(self):
        return self._casting_time

    @property
    def concentration(self):
        return self._concentration

    @property
    def duration(self):
        return self._duration

    @property
    def range(self):
        return self._range

    @property
    def components(self):
        return self._components

    @property
    def damage(self):
        return self._damage

    @property
    def duration(self):
        return self._duration

    @property
    def higher_level(self):
        return self._higher_level

    @property
    def description(self):
        return self._description

    @property
    def material(self):
        return self._material

    @property
    def ritual(self):
        return self._ritual

class SpellDamage:
    def __init__(self, **kwargs):
        allowed_attributes = ['damage_at_slot_level', 'type']
        __slots__ = '_damage_at_slot_level', '_type'

        self._damage_at_slot_level = []
        self._type = None

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    # TODO: create class to seperate dice count and dice type from the xdx string
    @property
    def damage_at_slot_level(self):
        return self._damage_at_slot_level

    @property
    def type(self):
        return self._type
