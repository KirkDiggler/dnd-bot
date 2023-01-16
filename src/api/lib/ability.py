class AbilityScore:
    def __init__(self, key: str, name: str, skills: list):
        __slots__ = '_key', '_name', '_skills'

        self._key = key
        self._name = name
        self._skills = skills

    def __str__(self):
        return f'{self._key}: {self._name}'

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @property
    def skills(self):
        return self._skills

class AbilityBonus:
    def __init__(self, ability_score: AbilityScore, bonus: int):
        __slots__ = '_ability_score', '_bonus'

        self._ability_score = ability_score
        self._bonus = bonus

    def __str__(self):
        return f'{self._ability.name}: {self._bonus}'

    @property
    def ability_score(self):
        return self._ability_score

    @property
    def bonus(self):
        return self._bonus