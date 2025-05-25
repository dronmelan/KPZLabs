from typing import List
from ..utils.enums import AnimalType

class Food:
    def __init__(self, name: str, nutrition_value: int, suitable_for: List[AnimalType]):
        if not name:
            raise ValueError("Food name cannot be empty")
        if nutrition_value <= 0:
            raise ValueError("Nutrition value must be positive")

        self._name = name
        self._nutrition_value = nutrition_value
        self._suitable_for = suitable_for

    @property
    def name(self) -> str:
        return self._name

    @property
    def nutrition_value(self) -> int:
        return self._nutrition_value

    def is_suitable_for(self, animal_type: AnimalType) -> bool:
        return animal_type in self._suitable_for