from enum import Enum
from src.api.lib import choice, referencelib

class ReferenceType(Enum):
    EQUIPMENT = "equipment"
    SPELL = "spells"
    MAGIC_ITEM = "magic-items"
    CLASS = "classes"
    SUBRACE = "subraces"
    RACE = "races"
    TRAIT = "traits"
    ABILITY_SCORE = "ability-scores"
    CONDITION = "conditions"
    DAMAGE_TYPE = "damage-types"
    EQUIPMENT_CATEGORY = "equipment-categories"
    LANGUAGE = "languages"
    MONSTER = "monsters"
    PROFICIENCY = "proficiencies"
    WEAPON_PROPERTY = "weapon-properties"
    SKILL = "skills"
    FEATURE = "features"


class Cost:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def __str__(self):
        return f"{self.quantity} {self.unit}"

class Choice:
    def __init__(self, *initial_data, **kwargs):
        self.chosen = 0
        for dictionary in initial_data:
            for key in dictionary:
                if key == "from":
                    setattr(self, 'from_', dictionary[key])
                    if dictionary[key]['option_set_type'] == 'options_array':
                        setattr(self, "choose_type", "options_array")
                        setattr(self, "choose_from", OptionsArrayOptionSet(dictionary[key]))
                    elif dictionary[key]['option_set_type'] == 'equipment_category':
                        setattr(self, "choose_type", "equipment_category")
                        # We set a reference item here because the client will
                        setattr(self, "choose_from", ReferenceOption(dictionary[key]['equipment_category']))
                else:
                    setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        return self.desc

    def select(self, reference_index: str):
        if self.chosen >= self.choose:
            raise Exception("You have already chosen the maximum number of options from this choice")

        self.chosen += 1

        return self.choose_from.select(reference_index)

    def to_model(self):
        choice = choice.Choice(
            choose=self.choose,

        )

def _choice_from_to_model(input):
    return choice.Choice(
        choose=input.choose,
        _option_list=input.choose_from.to_model(),
    )

class Option:
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
                if key == "option_type":
                    if dictionary[key] == "choice":
                        setattr(self, "option", Choice(dictionary["choice"]))
                    elif dictionary[key] == "reference":
                        setattr(self, "option", ReferenceOption(dictionary["item"]))
                    elif dictionary[key] == "counted_reference":
                        setattr(self, "option", ReferenceOption(dictionary["of"]))

        for key in kwargs:
            setattr(self, key, kwargs[key])
        
    def __str__(self):
        return f"option type: {self.option_type}"

    def to_model(self):
        if self.option_type == "choice":
            return choice.Choice(
                option_type=self.option_type,
                option=_choice_from_to_model(self.option),
            )
        
        return choice.ReferenceOption(
            option_type=self.option_type,
            option=self.option.item.to_model(self),
        )
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
    elif input == ReferenceType.CLASS:
        return referencelib.ReferenceType.CLASS
    elif input == ReferenceType.FEATURE:
        return referencelib.ReferenceType.FEATURE
    elif input == ReferenceType.SUBRACE:
        return referencelib.ReferenceType.SUBRACE
    elif input == ReferenceType.SPELL:
        return referencelib.ReferenceType.SPELL
    return referencelib.ReferenceType(
        value=input.value,
    )

class ReferenceItem:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "url": # The url is in format api/type/name
                    url = dictionary[key].split("/")
                    setattr(self, "reference_type", ReferenceType(url[2]))
                    setattr(self, "key", url[3])
                else:
                    setattr(self, key, dictionary[key])

    def __str__(self):
        return self.name

    def to_model(self):
        return referencelib.ReferenceItem(
            key=self.index,
            name=self.name,
            type=_reference_type_to_model(self.reference_type),
        )

class ReferenceOption:
    def __init__(self, *initial_data, **kwargs):
            for dictionary in initial_data:
                self.item = ReferenceItem(initial_data[0])

            for key in kwargs:
                setattr(self, key, kwargs[key])

    def __str__(self):
        return f"{self.option_type}"

    def select(self):
        return self.item

class OptionsArrayOptionSet:
    def __init__(self, *initial_data, **kwargs):
        self.current_idx = 0
        for dictionary in initial_data:
            for key in dictionary:
                if key == "options":
                    setattr(self, key, [Option(o) for o in dictionary[key]])
                else:
                    setattr(self, key, dictionary[key])

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def select(self, reference_index):
        for option in self.options:
            if option.option_type == "reference" or option.option_type == "counted_reference":
                if option.option.item.index == reference_index:
                    if hasattr(option.option, 'chosen'):
                        raise Exception("You have already chosen this option")

                    setattr(option.option, "chosen", True)
                    return option.option.select()
            elif option.option_type == "choice":
                selected = option.option.select(reference_index)
                if selected:
                    return selected

    def to_model(self):
        return choice.OptionList(
            select_from=[o.to_model() for o in self.options],
        )
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.current_idx >= len(self.options):
            raise StopIteration

        self.current_idx += 1
        return self.options[self.current_idx - 1]
    