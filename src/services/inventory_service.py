from typing import List, Dict, Any
from ..models.animal import Animal
from ..models.enclosure import Enclosure
from ..models.employee import Employee
from ..models.food import Food
from ..utils.enums import AnimalType

class InventoryService:
    def __init__(self):
        self._animals: List[Animal] = []
        self._enclosures: List[Enclosure] = []
        self._employees: List[Employee] = []
        self._food_inventory: List[Food] = []

    # Open/Closed Principle - methods can be extended without modification
    def add_animal(self, animal: Animal) -> None:
        if not isinstance(animal, Animal):
            raise TypeError("Expected Animal instance")
        self._animals.append(animal)

    def add_enclosure(self, enclosure: Enclosure) -> None:
        if not isinstance(enclosure, Enclosure):
            raise TypeError("Expected Enclosure instance")
        self._enclosures.append(enclosure)

    def add_employee(self, employee: Employee) -> None:
        if not isinstance(employee, Employee):
            raise TypeError("Expected Employee instance")
        self._employees.append(employee)

    def add_food(self, food: Food) -> None:
        if not isinstance(food, Food):
            raise TypeError("Expected Food instance")
        self._food_inventory.append(food)

    def get_animal_count(self) -> int:
        return len(self._animals)

    def get_employee_count(self) -> int:
        return len(self._employees)

    def get_enclosure_count(self) -> int:
        return len(self._enclosures)

    def get_animals_by_type(self, animal_type: AnimalType) -> List[Animal]:
        return [animal for animal in self._animals if animal.animal_type == animal_type]

    def find_animal_by_name(self, name: str) -> Animal:
        for animal in self._animals:
            if animal.name.lower() == name.lower():
                return animal
        raise ValueError(f"Animal with name '{name}' not found")

    def find_enclosure_by_id(self, enclosure_id: str) -> Enclosure:
        for enclosure in self._enclosures:
            if enclosure.id == enclosure_id:
                return enclosure
        raise ValueError(f"Enclosure with ID '{enclosure_id}' not found")

    def get_inventory_summary(self) -> Dict[str, Any]:
        return {
            "total_animals": self.get_animal_count(),
            "total_employees": self.get_employee_count(),
            "total_enclosures": self.get_enclosure_count(),
            "animals_by_type": {
                animal_type.value: len(self.get_animals_by_type(animal_type))
                for animal_type in AnimalType
            }
        }
    pass