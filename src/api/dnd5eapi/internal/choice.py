from src.api.lib import choicelib
from src.api.lib import referencelib
from .common import ReferenceType, ReferenceItem

class Choice:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == 'from':
                    setattr(self, 'from_', dictionary[key])
                else:
                    setattr(self, key, dictionary[key])

    def __str__(self):
        return f"{self.__dict__}"

    def to_model(self):
        if self.from_['option_set_type'] == 'options_array':
            return choicelib.Choice(
                choose=self.choose,
                option_list=OptionSet(self.from_['options']).to_model(),
            )
        else:
            raise Exception("option_set_type Not implemented")

def _reference_type_to_model(input):
    if input == ReferenceType.PROFICIENCY:
        return referencelib.ReferenceType.PROFICIENCY
    elif input == ReferenceType.LANGUAGE:
        return referencelib.ReferenceType.LANGUAGE
    elif input == ReferenceType.SKILL:
        return referencelib.ReferenceType.SKILL
    elif input == ReferenceType.ABILITY_SCORE:
        return referencelib.ReferenceType.ABILITY_SCORE
    elif input == ReferenceType.DAMAGE_TYPE:
        return referencelib.ReferenceType.DAMAGE_TYPE
    elif input == ReferenceType.CONDITION:
        return referencelib.ReferenceType.CONDITION
    elif input == ReferenceType.EQUIPMENT_CATEGORY:
        return referencelib.ReferenceType.EQUIPMENT_CATEGORY
    elif input == ReferenceType.WEAPON_PROPERTY:
        return referencelib.ReferenceType.WEAPON_PROPERTY
    elif input == ReferenceType.RACE:
        return referencelib.ReferenceType.RACE
    return referencelib.ReferenceType(
        value=input.value,
    )

class OptionSet:
    def __init__(self, options):
        self.options = options

    def __str__(self):
        return f"{self.__dict__}"


    def to_model(self):
        return choicelib.OptionList(
            select_from=[Option(option).to_model() for option in self.options],
        )

class ReferenceOption:
    def __init__(self, *initial_data):
        self.item = ReferenceItem(initial_data[0])

    def __str__(self):
        return f"{self.__dict__}"

    def to_model(self):
        return choicelib.ReferenceOption(
            # TODO: get the type from url and convert to modle ReferenceType
            item=self.item.to_model(),
        )

class MultipleReferenceOptions:
    def __init__(self, *initial_data):
        self.items = [Option(item) for item in initial_data[0]]

    def __str__(self):
        return f"{self.__dict__}"

    def to_model(self):
        return choicelib.MultipleReferenceOptions(
            items=[item.to_model() for item in self.items],
        )

class Option:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
                if key == 'option_type':
                    if dictionary[key] == 'choice':
                        setattr(self, 'option', Choice(dictionary['choice']))
                    elif dictionary[key] == 'reference':
                        setattr(self, 'option', ReferenceOption(dictionary['item']))
                    elif dictionary[key] == 'counted_reference':
                        setattr(self, 'option', ReferenceOption(dictionary['of']))
                    elif dictionary[key] == 'multiple':
                        setattr(self, 'option', MultipleReferenceOptions(dictionary['items']))

    def __str__(self):
        return f"{self.__dict__}"

    def to_model(self):
        return self.option.to_model()
