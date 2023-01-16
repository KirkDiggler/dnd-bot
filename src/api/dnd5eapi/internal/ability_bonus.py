from .ability_score import AbilityScore
from src.api.lib import ability

class AbilityBonus:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "ability_score":
                    setattr(self, key, AbilityScore(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])

    def to_dict(self):
        return {
            "ability_score": self.ability_score.index,
            "bonus": self.bonus
        }

    def to_model(self):
        return ability.AbilityBonus(
            ability_score=self.ability_score.to_model(),
            bonus=self.bonus,
        )