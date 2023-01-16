from enum import Enum
from .common import Cost, ReferenceItem
from src.api.lib import equipmentlib, weapon, armor, cost, damage
class EquipmentCategoryType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ADVENTURING_GEAR = "adventuring-gear"
    TOOL = "tools"
    MOUNT = "mount"

class EquipmentCategory:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "index":
                    setattr(self, "type_", EquipmentCategoryType(dictionary[key]))
                else:
                    setattr(self, key, dictionary[key])

# General Equipment
class Equipment:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "properties":
                    setattr(self, key, [ReferenceItem(prop) for prop in dictionary[key]])

                setattr(self, key, dictionary[key])

    def to_model(self):
        weight = 0
        if hasattr(self, 'weight'):
            weight = self.weight
        return equipmentlib.Equipment(
            key=self.index,
            name=self.name,
            category=_category_to_model(self.equipment_category['index']),
            cost=cost.Cost(quantity=self.cost['quantity'], unit=cost.CostUnit(self.cost['unit'])),
            weight=weight,
            desc=self.desc,
            contents=self.contents,
            properties=[prop.to_model() for prop in self.properties],
        )
# TODO: leverage the super class
class EquipmentArmor(Equipment):
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "properties":
                    setattr(self, key, [ReferenceItem(prop) for prop in dictionary[key]])
                else:
                    setattr(self, key, dictionary[key])

    def to_model(self):
        return armor.Armor(
            key=self.index,
            name=self.name,
            category=_category_to_model(self.equipment_category['index']),
            cost=cost.Cost(quantity=self.cost['quantity'], unit=cost.CostUnit(self.cost['unit'])),
            weight=self.weight,
            desc=self.desc,
            armor_category=_armor_category_to_model(self.armor_category),
            armor_class=armor.ArmorClass(base=self.armor_class['base'],
                                         dex_bonus=self.armor_class['dex_bonus']),
            str_minimum=self.str_minimum,
            stealth_disadvantage=self.stealth_disadvantage,
            properties=[prop.to_model() for prop in self.properties]
        )

# This function allows us to have different enum values for the API and the models
def _category_to_model(category):
    return equipmentlib.EquipmentCategory(category)

def _armor_category_to_model(category):
    print(category)

    lookup = {
        'Heavy': armor.ArmorCategory.HEAVY,
        'Medium': armor.ArmorCategory.MEDIUM,
        'Light': armor.ArmorCategory.LIGHT,
        'Shield': armor.ArmorCategory.SHIELD
    }

    return lookup[category]

class EquipmentWeapon(Equipment):
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "properties":
                    setattr(self, key, [ReferenceItem(prop) for prop in dictionary[key]])
                else:
                    setattr(self, key, dictionary[key])

    def to_model(self):
        # TODO: protect against invalid dice strings
        dice_parts = self.damage['damage_dice'].split("d")
        if hasattr(self, 'two_handed_damage'):
            two_handed_dice_parts = self.two_handed_damage['damage_dice'].split("d")
            two_handed_damage_type = self.two_handed_damage['damage_type']['index']
        else:
            two_handed_dice_parts = [0, 0]
            two_handed_damage_type = None
        
        return weapon.Weapon(
            key=self.index,
            name=self.name,
            category=_category_to_model(self.equipment_category['index']),
            cost=cost.Cost(quantity=self.cost['quantity'], unit=cost.CostUnit(self.cost['unit'])),
            weight=self.weight,
            desc=self.desc,
            weapon_category=_weapon_category_to_model(self.weapon_category),
            weapon_range=self.weapon_range,
            category_range=self.category_range,
            properties=[prop.to_model() for prop in self.properties],
            range=self.range,
            damage=damage.Damage(dice_count=int(dice_parts[0]),
                                 dice_type=int(dice_parts[1]),
                                 type=self.damage['damage_type']['index']),
            two_handed_damage=damage.Damage(dice_count=int(two_handed_dice_parts[0]),
                                            dice_type=int(two_handed_dice_parts[1]),
                                            type=two_handed_damage_type)
        )

def _weapon_category_to_model(category):
    lookup = {
        'Simple': weapon.WeaponCategory.SIMPLE,
        'Simple Melee': weapon.WeaponCategory.SIMPLE_MELEE,
        'Simple Ranged': weapon.WeaponCategory.SIMPLE_RANGED,
        'Martial Melee': weapon.WeaponCategory.MARTIAL_MELEE,
        'Martial Ranged': weapon.WeaponCategory.MARTIAL_RANGED,
        'Martial': weapon.WeaponCategory.MARTIAL
    }
    return lookup[category]