from typing import Dict, Any
from .food import Food
from ..interfaces.base_interfaces import Feedable, Observable
from ..utils.enums import AnimalType

class Animal(Feedable, Observable):
    def __init__(self, name: str, species: str, age: int, animal_type: AnimalType):
        # Fail Fast - validate inputs immediately
        if not name or not species:
            raise ValueError("Name and species cannot be empty")
        if age < 0:
            raise ValueError("Age cannot be negative")

        self._name = name
        self._species = species
        self._age = age
        self._animal_type = animal_type
        self._hunger_level = 50  # 0-100 scale
        self._health_status = "healthy"

    @property
    def name(self) -> str:
        return self._name

    @property
    def species(self) -> str:
        return self._species

    @property
    def age(self) -> int:
        return self._age

    @property
    def animal_type(self) -> AnimalType:
        return self._animal_type

    def feed(self, food: 'Food') -> bool:
        if food.is_suitable_for(self._animal_type):
            self._hunger_level = max(0, self._hunger_level - food.nutrition_value)
            return True
        return False

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self._name,
            "species": self._species,
            "age": self._age,
            "type": self._animal_type.value,
            "hunger_level": self._hunger_level,
            "health": self._health_status
        }
    pass

class Mammal(Animal):
    def __init__(self, name: str, species: str, age: int, fur_color: str = "brown"):
        super().__init__(name, species, age, AnimalType.MAMMAL)
        self._fur_color = fur_color
    pass

class Bird(Animal):
    def __init__(self, name: str, species: str, age: int, can_fly: bool = True):
        super().__init__(name, species, age, AnimalType.BIRD)
        self._can_fly = can_fly

    def fly(self) -> str:
        return f"{self.name} is flying!" if self._can_fly else f"{self.name} cannot fly"
    pass

class Reptile(Animal):
    def __init__(self, name: str, species: str, age: int, is_venomous: bool = False):
        super().__init__(name, species, age, AnimalType.REPTILE)
        self._is_venomous = is_venomous
    pass