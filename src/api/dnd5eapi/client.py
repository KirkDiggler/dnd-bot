import os
import requests_cache
import requests
from .internal.common import ReferenceItem
from .internal.choice import Choice
from .internal.character_class import CharacterClass
from .internal.level import Level
from .internal.equipment import Equipment, EquipmentWeapon, EquipmentArmor, EquipmentCategory, EquipmentCategoryType
from .internal.race import Race
from .internal.trait import Trait
from .internal.skill import Skill
from .internal.proficiency import Proficiency
from .internal.spell import Spell

class Client:
    def __init__(self, cache_path: str = 'dnd5eapi_cache'):
        self.base_url = 'https://www.dnd5eapi.co/api'
        root = os.path.dirname(os.path.dirname(__file__))
        self.session = requests_cache.CachedSession(os.path.join(root, cache_path))

    def close(self):
        self.session.close()

    def _query(self, path: str, params: dict = None) -> dict:
        url = f"{self.base_url}/{path}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_class_levels(self, class_name: str) -> list[Level]:
        levels = self._query(f'classes/{class_name}/levels')
        return [Level(l) for l in levels]

    def list_classes(self) -> list[ReferenceItem]:
        return [ReferenceItem(c).to_model() for c in self._query('classes')['results']]

    def get_class(self, name: str) -> CharacterClass:
        class_ = CharacterClass(self._query(f'classes/{name}'))
        class_.class_levels = self.get_class_levels(name)

        # Find equipment_category options and load them into an array option
        # Not super happy with this but I believe it is safe and functional
        choices = []
        for choice_dict in class_.starting_equipment_options:
            choice = self._load_equipment_category_choices(choice_dict)

            choices.append(choice)

        class_.starting_equipment_options = choices

        return class_.to_model()

    def list_races(self) -> list[ReferenceItem]:
        return [ReferenceItem(r).to_model() for r in self._query('races')['results']]
    
    def get_race(self, name):
        return Race(self._query(f"races/{name}")).to_model()

    def get_skill(self, name):
        return Skill(self._query(f"skills/{name}"))

    def get_trait(self, name):
        return Trait(self._query(f"traits/{name}")).to_model()

    def get_proficiency(self, name):
        return Proficiency(self._query(f"proficiencies/{name}")).to_model()

    def list_spells(self, level: int = None, school: str = None, char_class: str = None, name: str = None) -> list[ReferenceItem]:
        params = {}
        if level is not None:
            params['level'] = level
        if school is not None:
            params['school'] = school
        if name is not None:
            params['name'] = [name]
        if char_class is not None:
            all_spell_keys = [key['index'] for key in self._query('spells', params=params)['results']]
            class_spells = []
            for s in self._query(f"classes/{char_class}/spells")['results']:
                if s['index'] in all_spell_keys:
                    class_spells.append(ReferenceItem(s))
            return class_spells
        else:
            return [ReferenceItem(s).to_model() for s in self._query('spells', params=params)['results']]

    def get_spell(self, name: str) -> dict:
        return Spell(self._query(f'spells/{name}')).to_model()

    def list_equipment_categories(self) -> list[EquipmentCategory]:
        return [EquipmentCategory(c) for c in self._query('equipment-categories')['results']]

    def list_equipment_by_category(self, category: str) -> list[ReferenceItem]:
        return [ReferenceItem(e) for e in self._query(f'equipment-categories/{category}')['equipment']]

    def get_equipment(self, name: str) -> Equipment:
        json = self._query(f'equipment/{name}')
        category = EquipmentCategory(json['equipment_category'])
        if category.type_ == EquipmentCategoryType.WEAPON:
            return EquipmentWeapon(json).to_model()
        elif category.type_ == EquipmentCategoryType.ARMOR:
            return EquipmentArmor(json).to_model()
        else:
            return Equipment(json).to_model()

    # Convert equipment_category choices into an array of equipment
    def _load_equipment_category_choices(self, choice) -> Choice:
        print(f"before: {choice}\n")
        if 'option_type' in choice and choice['option_type'] == 'choice':
            choice['choice'] = self._load_equipment_category_choices(choice['choice'])
        elif 'from' in choice and choice['from']['option_set_type'] == 'equipment_category':
            choice['from']['option_set_type'] = 'options_array'
            index = choice['from']['equipment_category']['index']
            equipment_list = self._query(f'equipment-categories/{index}')['equipment']
            options = [{'option_type': 'reference', 'item': {'index': c['index'], 'name': c['name'], 'url': c['url']}} for c in equipment_list]
            choice['from']['options'] = options
        elif  'from' in choice and choice['from']['option_set_type'] == 'options_array':
            for option in choice['from']['options']:
                if option['option_type'] == 'choice':
                    option['choice'] = self._load_equipment_category_choices(option['choice'])
                elif option['option_type'] ==  'multiple':
                    for item in option['items']:
                        item = self._load_equipment_category_choices(item)
        print(f"after: {choice}\n")

        return choice
