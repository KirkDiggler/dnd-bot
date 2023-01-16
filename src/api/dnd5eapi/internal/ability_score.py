from .common import ReferenceItem
from src.api.lib import ability

class AbilityScore:
    def __init__(self, *initial_data):
        # Set defaults for optional fields
        self.skills = []
        for dictionary in initial_data:
            for key in dictionary:
                if key == "skills":
                    setattr(self, key, [ReferenceItem(skill) for skill in dictionary[key]])

                setattr(self, key, dictionary[key])

    def to_model(self):
        return ability.AbilityScore(
            key=self.index,
            name=self.name,
            skills = [skill.to_model() for skill in self.skills],
        )
