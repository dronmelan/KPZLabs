from abc import ABC, abstractmethod

from task5.models.character import Character
from task5.models.enums import Gender, Build


class CharacterBuilder(ABC):

    def __init__(self):
        self.character = Character()

    def get_character(self) -> Character:
        result = self.character
        self.reset()
        return result

    def reset(self) -> 'CharacterBuilder':
        self.character = Character()
        return self

    def set_name(self, name: str) -> 'CharacterBuilder':
        self.character.name = name
        return self

    def set_gender(self, gender: Gender) -> 'CharacterBuilder':
        self.character.gender = gender
        return self

    def set_age(self, age: int) -> 'CharacterBuilder':
        self.character.age = age
        return self

    def set_height(self, height: int) -> 'CharacterBuilder':
        self.character.height = height
        return self

    def set_build(self, build: Build) -> 'CharacterBuilder':
        self.character.build = build
        return self

    def set_hair_color(self, color: str) -> 'CharacterBuilder':
        self.character.hair_color = color
        return self

    def set_eye_color(self, color: str) -> 'CharacterBuilder':
        self.character.eye_color = color
        return self

    def set_skin_color(self, color: str) -> 'CharacterBuilder':
        self.character.skin_color = color
        return self

    def add_clothing(self, item_type: str, item: str) -> 'CharacterBuilder':
        self.character.clothing[item_type] = item
        return self

    def add_weapon(self, weapon: str) -> 'CharacterBuilder':
        self.character.weapons.append(weapon)
        return self

    def add_armor(self, armor: str) -> 'CharacterBuilder':
        self.character.armor.append(armor)
        return self

    def add_accessory(self, accessory: str) -> 'CharacterBuilder':
        self.character.accessories.append(accessory)
        return self

    def add_inventory_item(self, item: str) -> 'CharacterBuilder':
        self.character.inventory.append(item)
        return self

    def set_gold(self, amount: int) -> 'CharacterBuilder':
        self.character.gold = amount
        return self

    def add_skill(self, skill: str, level: int) -> 'CharacterBuilder':
        self.character.skills[skill] = level
        return self

    def add_special_ability(self, ability: str) -> 'CharacterBuilder':
        self.character.special_abilities.append(ability)
        return self

    def set_backstory(self, story: str) -> 'CharacterBuilder':
        self.character.backstory = story
        return self

    def add_personality_trait(self, trait: str) -> 'CharacterBuilder':
        self.character.personality_traits.append(trait)
        return self

    def add_fear(self, fear: str) -> 'CharacterBuilder':
        self.character.fears.append(fear)
        return self

    def add_goal(self, goal: str) -> 'CharacterBuilder':
        self.character.goals.append(goal)
        return self

    @abstractmethod
    def build_moral_alignment(self) -> 'CharacterBuilder':
        pass

    @abstractmethod
    def add_moral_deed(self, deed: str) -> 'CharacterBuilder':
        pass