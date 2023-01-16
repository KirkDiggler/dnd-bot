from .ability_bonus import AbilityBonus
from .common import Choice, ReferenceItem
from .proficiency import Proficiency
from .trait import Trait

from src.api.lib import racelib
 
class Race:
    def __init__(self, *initial_data):
        # Set defaults for optional fields
        self.ability_bonuses = []
        self.ability_bonus_options = []
        self.proficiencies = []
        self.starting_proficiency_options = []
        self.languages = []
        self.language_options = []
        self.traits = []
        self.subraces = []
        
        self.current_idx = 0
        for dictionary in initial_data:
            for key in dictionary:
                if key == "ability_bonuses":
                    setattr(self, key, [AbilityBonus(a) for a in dictionary[key]])
                elif key == "ability_bonus_options":
                    setattr(self, key, Choice(dictionary[key]))
                elif key == "starting_proficiencies":
                    setattr(self, key, [ReferenceItem(p) for p in dictionary[key]])
                elif key == "ability_bonus_options":
                    setattr(self, key, Choice(dictionary[key]))
                elif key == "starting_proficiency_options":
                    setattr(self, key, Choice(dictionary[key]))
                elif key == "languages":
                    setattr(self, key, [ReferenceItem(l) for l in dictionary[key]])
                elif key == "language_options":
                    setattr(self, key, Choice(dictionary[key]))
                elif key == "traits":
                    setattr(self, key, [Trait(t) for t in dictionary[key]])
                elif key == "subraces":
                    setattr(self, key, [ReferenceItem(r) for r in dictionary[key]])
                else:
                    setattr(self, key, dictionary[key])

    def __str__(self):
        return self.name

    def to_model(self):
        language_options = None
        if hasattr(self, 'language_options'):
            language_options = self.language_options.to_model()
        
        starting_proficiency_options = None
        if hasattr(self, 'starting_proficiency_options'):
            starting_proficiency_options = self.starting_proficiency_options.to_model()

        ability_bonus_options = None
        if hasattr(self, 'ability_bonus_options'):
            ability_bonus_options = self.ability_bonus_options.to_model()

        return racelib.Race(
            key=self.index,
            name=self.name,
            ability_bonuses=[a.to_model() for a in self.ability_bonuses],
            ability_bonus_options=ability_bonus_options,
            age=self.age,
            alignment=self.alignment,
            size=self.size,
            speed=self.speed,
            size_description=self.size_description,
            starting_proficiencies=[p.to_model() for p in self.starting_proficiencies],
            starting_proficiency_options=starting_proficiency_options,
            languages=[l.to_model() for l in self.languages],
            language_options = language_options,
            language_desc=self.language_desc,
            traits=[t.to_model() for t in self.traits], # returns reference item for now
            subraces=[r.to_model() for r in self.subraces]
        )
