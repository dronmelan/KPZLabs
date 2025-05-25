from typing import Dict, Any
from ..services.inventory_service import InventoryService

class Zoo:
    def __init__(self, name: str, inventory_service: InventoryService):
        if not name:
            raise ValueError("Zoo name cannot be empty")

        self._name = name
        self._inventory = inventory_service  # Dependency injection

    @property
    def name(self) -> str:
        return self._name

    def add_animal_to_enclosure(self, animal_name: str, enclosure_id: str) -> bool:
        try:
            animal = self._inventory.find_animal_by_name(animal_name)
            enclosure = self._inventory.find_enclosure_by_id(enclosure_id)
            return enclosure.add_animal(animal)
        except ValueError:
            return False

    def get_zoo_status(self) -> Dict[str, Any]:
        return {
            "zoo_name": self._name,
            "inventory": self._inventory.get_inventory_summary()
        }
    pass