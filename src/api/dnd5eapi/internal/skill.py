from .ability_score import AbilityScore

class Skill:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "ability_score":
                    setattr(self, key, AbilityScore(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])
