from typing import List, Dict, Any
from ..interfaces.base_interfaces import Maintainable, Observable
from ..utils.enums import EnclosureType, AnimalType
from .animal import Animal

class Enclosure(Maintainable, Observable):
    def __init__(self, enclosure_id: str, enclosure_type: EnclosureType,
                 capacity: int, size_sqm: float):
        if not enclosure_id:
            raise ValueError("Enclosure ID cannot be empty")
        if capacity <= 0 or size_sqm <= 0:
            raise ValueError("Capacity and size must be positive")

        self._id = enclosure_id
        self._type = enclosure_type
        self._capacity = capacity
        self._size_sqm = size_sqm
        self._animals: List[Animal] = []
        self._cleanliness_level = 100  # 0-100 scale

    @property
    def id(self) -> str:
        return self._id

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def current_occupancy(self) -> int:
        return len(self._animals)

    def add_animal(self, animal: Animal) -> bool:
        if self.current_occupancy >= self._capacity:
            return False

        if self._is_compatible_animal_type(animal.animal_type):
            self._animals.append(animal)
            return True
        return False

    def remove_animal(self, animal: Animal) -> bool:
        if animal in self._animals:
            self._animals.remove(animal)
            return True
        return False

    def _is_compatible_animal_type(self, animal_type: AnimalType) -> bool:
        # DRY principle - centralized compatibility logic
        compatibility_map = {
            EnclosureType.CAGE: [AnimalType.MAMMAL, AnimalType.REPTILE],
            EnclosureType.AVIARY: [AnimalType.BIRD],
            EnclosureType.AQUARIUM: [AnimalType.FISH],
            EnclosureType.OPEN_AREA: [AnimalType.MAMMAL]
        }
        return animal_type in compatibility_map.get(self._type, [])

    def maintain(self) -> bool:
        self._cleanliness_level = 100
        return True

    def get_status(self) -> Dict[str, Any]:
        return {
            "id": self._id,
            "type": self._type.value,
            "capacity": self._capacity,
            "occupancy": self.current_occupancy,
            "size_sqm": self._size_sqm,
            "cleanliness": self._cleanliness_level,
            "animals": [animal.name for animal in self._animals]
        }

    def get_animals(self) -> List[Animal]:
        return self._animals.copy()  # Return copy to prevent external modification