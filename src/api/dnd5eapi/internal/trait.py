from .common import Choice, ReferenceItem
from src.api.lib import referencelib

class TraitSpecific:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key.endswith('_options'):
                    setattr(self, key, Choice(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])

class Trait:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "trait_specific":
                    setattr(self, key, TraitSpecific(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])
    
    def __str__(self):
        return self.name

    def to_model(self):
        return referencelib.ReferenceItem(
            key=self.index,
            name=self.name,
            type=referencelib.ReferenceType.TRAIT,
        )
