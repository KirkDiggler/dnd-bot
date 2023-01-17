class Level:
    def __init__(self, **kwargs):
        self._features = []
        self._spell_slots = None
        
        allowed_attributes = ['level', 'ability_score_bonuses', 'proficiency_bonus', 'features', 'spellcasting', 'spell_slots']
        __slots__ = '_level', '_ability_score_bonuses', '_proficiency_bonus', '_features', '_spellcasting', '_spell_slots'

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

    @property
    def level(self):
        return self._level

    @property
    def ability_score_bonuses(self):
        return self._ability_score_bonuses

    @property
    def proficiency_bonus(self):
        return self._proficiency_bonus

    @property
    def features(self):
        return self._features

    @property
    def spellcasting(self):
        return self._spellcasting

    @property
    def spell_slots(self):
        return self._spell_slots
